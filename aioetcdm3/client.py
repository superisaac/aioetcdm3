from typing import Union, Optional, Any, List, Tuple, Dict, Type, AsyncGenerator
import logging
from urllib.parse import urlparse
import asyncio
from asyncio import Queue

from random import choice
from functools import wraps

from grpclib.client import Channel, Stream
from grpclib.exceptions import StreamTerminatedError

from aioetcdm3.pb.etcdserverpb import rpc_pb2 as pb2
from aioetcdm3.pb.mvccpb import kv_pb2
from aioetcdm3.pb.etcdserverpb.rpc_grpc import (
    KVStub, WatchStub, LeaseStub, ClusterStub,
    MaintenanceStub, AuthStub)

from .utils import ensure_bytes, prefix_range_end

logger = logging.getLogger(__name__)

KeyRange = Union[str, bytes, Tuple[Union[bytes, str], Union[bytes, str]]]

class Client:
    channel: Channel
    status: str = 'alive'
    _kv: Optional['KVSection'] = None
    _lease: Optional['LeaseSection'] = None
    _watch: Optional['WatchSection'] = None
    _cluster: Optional['ClusterSection'] = None
    _server_urls: List[str]
    _current_server_url: str = ''
    _etcd_args: Dict[str, Any]

    def __init__(self, server_url, **kwargs):
        self._server_urls = [server_url]
        self._etcd_args = kwargs
        self.select_server()

    def select_server(self):
        assert self._server_urls
        self._current_server_url = choice(self._server_urls)
        logger.info('selected etcd server %s', self._current_server_url)
        parsed = urlparse(self._current_server_url)
        if ':' in parsed.netloc:
            host, port = parsed.netloc.split(':')
            port = int(port)
        else:
            host = parsed.netloc
            port = 2379
        # TODO: handle ssl
        self.channel = Channel(host, port, **self._etcd_args)

    def is_alive(self) -> bool:
        return self.status == 'alive'

    def close(self) -> None:
        self.status = 'closed'
        self.channel.close()
        print('cccc')

    async def collect_members(self, sleep_interval: float=60.0):
        '''\
        Periodly collect members, when one member failed, try to connect
        others.
        '''
        while self.is_alive():
            try:
                server_urls = []
                for member in await self.cluster.list_members():
                    server_urls.extend(member.clientURLs)
                    self._server_urls = server_urls
                    logger.info('current members %s', self._server_urls)
                await asyncio.sleep(sleep_interval)
            except RuntimeError as e:
                print('runtime error', e)
                logging.warning('runtime error %s', e)
                break

    @property
    def kv(self) -> 'KVSection':
        if self._kv is None:
            self._kv = KVSection(self)
        return self._kv

    @property
    def lease(self) -> 'LeaseSection':
        if self._lease is None:
            self._lease = LeaseSection(self)
        return self._lease

    @property
    def watch(self) -> 'WatchSection':
        if self._watch is None:
            self._watch = WatchSection(self)
        return self._watch

    @property
    def cluster(self) -> 'ClusterSection':
        if self._cluster is None:
            self._cluster = ClusterSection(self)
        return self._cluster


class ClientSection:
    client: 'Client'
    stub_cls: Type

    def __init__(self, client: 'Client'):
        self.client = client

    @property
    def stub(self) -> Any:
        return self.stub_cls(self.client.channel)

def section_retry(n:int=10):
    def outer(func):
        @wraps(func)
        async def wrapped(section, *args, **kwargs) -> Any:
            for retry_times in range(n):
                try:
                    return await func(section, *args, **kwargs)
                except OSError:
                    if retry_times < n - 1:
                        logger.warning('etcd function %s failed, retry times %s',
                                       func, retry_times)
                        await asyncio.sleep(1)
                        section.client.select_server()
                    else:
                        raise
        return wrapped
    return outer

class KVSection(ClientSection):
    stub_cls = KVStub

    @section_retry()
    async def put(self,
                  key: Union[bytes, str],
                  value: Union[bytes, str],
                  lease_id: int=0,
                  expect_prev_value: Optional[bytes]=None
                  ) -> bool:
        '''
        :return: the put is success or not
        '''
        key = ensure_bytes(key)
        value = ensure_bytes(value)

        req = pb2.PutRequest(
            key=key,
            value=value,
            lease=lease_id
        )
        if expect_prev_value is None:
            resp = await self.stub.Put(req)
            return True
        else:
            expect_prev_value = ensure_bytes(expect_prev_value)
            txnreq = pb2.TxnRequest(
                compare=[pb2.Compare(
                    result=pb2.Compare.CompareResult.EQUAL,
                    target=pb2.Compare.CompareTarget.VALUE,
                    key=key,
                    value=expect_prev_value
                )],
                success=[pb2.RequestOp(request_put=req)]
            )
            txnresp = await self.stub.Txn(txnreq)
            return txnresp.succeeded

    async def get(self,
                  key: Union[bytes, str]) -> Optional[bytes]:
        key = ensure_bytes(key)

        resp = await self.get_range(key, b"")
        if resp.kvs:
            return resp.kvs[0].value
        else:
            return None

    @section_retry()
    async def get_range(self,
                        start: Union[bytes, str],
                        end: Union[bytes, str],
                        limit: int=0,
                        sort_by: str='') -> pb2.RangeResponse:
        start = ensure_bytes(start)

        end = ensure_bytes(end)

        if not sort_by:
            sort_order = pb2.RangeRequest.SortOrder.NONE
            sort_t = 'key'
        elif sort_by.startswith('-'):
            sort_order = pb2.RangeRequest.SortOrder.DESCEND
            sort_t = sort_by[1:]
        else:
            sort_order = pb2.RangeRequest.SortOrder.ASCEND
            sort_t = sort_by

        assert sort_t.lower() in ('key', 'version', 'create', 'mod', 'value')

        sort_target = getattr(pb2.RangeRequest.SortTarget,
                              sort_t.upper())

        resp = await self.stub.Range(
            pb2.RangeRequest(
                key=start,
                range_end=end,
                limit=limit,
                sort_order=sort_order,
                sort_target=sort_target
            ))
        return resp

    async def delete(self,
                     key: Union[bytes, str],
                     prev_kv: bool = False) -> Optional[bytes]:
        key = ensure_bytes(key)

        resp = await self.delete_range(key, b"", prev_kv=prev_kv)
        if resp.prev_kvs:
            return resp.prev_kvs[0].value
        else:
            return None

    @section_retry()
    async def delete_range(self,
                           start: Union[bytes, str],
                           end: Union[bytes, str],
                           prev_kv: bool = False) ->  pb2.DeleteRangeResponse:
        start = ensure_bytes(start)
        end = ensure_bytes(end)

        resp = await self.stub.DeleteRange(
            pb2.DeleteRangeRequest(
                key=start,
                range_end=end,
                prev_kv=prev_kv))
        return resp

class LeaseSection(ClientSection):
    stub_cls = LeaseStub

    @section_retry()
    async def grant(self, ttl: int, lease_id: int=0) -> pb2.LeaseGrantResponse:
        resp = await self.stub.LeaseGrant(
            pb2.LeaseGrantRequest(
                TTL=ttl,
                ID=lease_id))
        return resp

    @section_retry()
    async def revoke(self, lease_id: int) -> pb2.LeaseRevokeResponse:
        return await self.stub.LeaseRevoke(
            pb2.LeaseRevokeRequest(
                ID=lease_id))

    @section_retry()
    async def keep_alive(self, *lease_ids:int, sleep_interval:float=1) -> None:
        assert not not lease_ids, "lease id list cannot be empty"
        async with self.stub.LeaseKeepAlive.open() as stream:
            while self.client.is_alive():
                for lease_id in lease_ids:
                    await stream.send_message(
                        pb2.LeaseKeepAliveRequest(
                            ID=lease_id))
                for _ in lease_ids:
                    resp = await stream.recv_message()

                await asyncio.sleep(sleep_interval)

    # TODO: TimeToLive and Lease and Leases

class WatchSection(ClientSection):
    stub_cls = WatchStub

    async def keep_watching(self,
                            *key_ranges:KeyRange
    ) -> AsyncGenerator[pb2.WatchResponse, None]:
        while self.client.is_alive():
            try:
                async for resp in self.open_stream(*key_ranges):
                    yield resp
            except OSError as e:
                # ConnectionRefusedError
                logger.warning('watching failed, %s', e)
                self.client.select_server()
                await asyncio.sleep(1)

    async def open_stream(self,
                   *key_ranges:KeyRange
    ) -> AsyncGenerator[pb2.WatchResponse, None]:

        async with self.stub.Watch.open() as stream:
            logging.info('stream %s opened to watch %s', stream, key_ranges)

            #for key, range_end in key_ranges:
            for r in key_ranges:
                if isinstance(r, (str, bytes)):
                    key, range_end = ensure_bytes(r), ''
                else:
                    assert isinstance(r, (tuple, list))
                    key, range_end = r
                await stream.send_message(pb2.WatchRequest(
                    create_request=pb2.WatchCreateRequest(
                        key=ensure_bytes(key),
                        range_end=ensure_bytes(range_end))))

            watch_id: int = 0
            while self.client.is_alive():
                try:
                    resp = await stream.recv_message()
                except StreamTerminatedError:
                    logger.warning('stream watching terminated %s', stream)
                    break
                if resp.created:
                    watch_id = resp.watch_id
                elif resp.canceled:
                    await stream.send_request(end=True)
                    break
                else:
                    yield resp

class ClusterSection(ClientSection):
    stub_cls = ClusterStub

    @section_retry()
    async def list_members(self) -> List[pb2.Member]:
        resp = await self.stub.MemberList(
            pb2.MemberListRequest())
        return resp.members
