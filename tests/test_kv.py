import pytest
from aioetcdm3.client import Client
from aioetcdm3.utils import ensure_bytes, prefix_range_end

@pytest.mark.asyncio
async def test_put_get():
    c = Client('http://127.0.0.1')
    await c.kv.put("hello", "nice")

    r = await c.kv.get("hello")
    assert r == b'nice'

@pytest.mark.asyncio
async def test_range_put_get():
    c = Client('http://127.0.0.1')
    for i in range(5):
        await c.kv.put(f'what{i}', f'ok{i}')

    end = prefix_range_end(b'what')
    resp = await c.kv.get_range('what', end)
    assert len(resp.kvs) == 5
    for i in range(5):
        assert resp.kvs[i].value == ensure_bytes(f'ok{i}')

@pytest.mark.asyncio
async def test_delete():
    c = Client('http://127.0.0.1')
    for i in range(5):
        await c.kv.put(f'what{i}', f'ok{i}')


    resp = await c.kv.delete('what2', prev_kv=True)
    #assert resp.prev_kvs[0].value == 'ok2'
    assert resp == b'ok2'

    v = await c.kv.get('what2')
    assert v is None

    end = prefix_range_end(b'what')
    resp = await c.kv.delete_range('what', end, prev_kv=True)
    assert len(resp.prev_kvs) == 4
    assert resp.prev_kvs[0].value == b'ok0'
    assert resp.prev_kvs[1].value == b'ok1'
    assert resp.prev_kvs[2].value == b'ok3'
    assert resp.prev_kvs[3].value == b'ok4'


@pytest.mark.asyncio
async def test_prefix_range_end():
    assert prefix_range_end(b'86') == b'87'
    assert prefix_range_end(b'ab\xff1\xff') == b'ab\xff2\xff'
    assert prefix_range_end(b'\xff\xff') == b'\xff\xff'



