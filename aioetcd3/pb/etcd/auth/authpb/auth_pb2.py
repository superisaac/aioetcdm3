# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from aioetcd.pb.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='auth.proto',
  package='authpb',
  syntax='proto3',
  serialized_options=b'\310\342\036\001\340\342\036\001\320\342\036\001\310\341\036\000\320\341\036\000',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\nauth.proto\x12\x06\x61uthpb\x1a\x14gogoproto/gogo.proto\"%\n\x0eUserAddOptions\x12\x13\n\x0bno_password\x18\x01 \x01(\x08\"^\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\x0c\x12\x10\n\x08password\x18\x02 \x01(\x0c\x12\r\n\x05roles\x18\x03 \x03(\t\x12\'\n\x07options\x18\x04 \x01(\x0b\x32\x16.authpb.UserAddOptions\"\x83\x01\n\nPermission\x12)\n\x08permType\x18\x01 \x01(\x0e\x32\x17.authpb.Permission.Type\x12\x0b\n\x03key\x18\x02 \x01(\x0c\x12\x11\n\trange_end\x18\x03 \x01(\x0c\"*\n\x04Type\x12\x08\n\x04READ\x10\x00\x12\t\n\x05WRITE\x10\x01\x12\r\n\tREADWRITE\x10\x02\"?\n\x04Role\x12\x0c\n\x04name\x18\x01 \x01(\x0c\x12)\n\rkeyPermission\x18\x02 \x03(\x0b\x32\x12.authpb.PermissionB\x14\xc8\xe2\x1e\x01\xe0\xe2\x1e\x01\xd0\xe2\x1e\x01\xc8\xe1\x1e\x00\xd0\xe1\x1e\x00\x62\x06proto3'
  ,
  dependencies=[gogoproto_dot_gogo__pb2.DESCRIPTOR,])



_PERMISSION_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='authpb.Permission.Type',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='READ', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WRITE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='READWRITE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=269,
  serialized_end=311,
)
_sym_db.RegisterEnumDescriptor(_PERMISSION_TYPE)


_USERADDOPTIONS = _descriptor.Descriptor(
  name='UserAddOptions',
  full_name='authpb.UserAddOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='no_password', full_name='authpb.UserAddOptions.no_password', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=81,
)


_USER = _descriptor.Descriptor(
  name='User',
  full_name='authpb.User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='authpb.User.name', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='authpb.User.password', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='roles', full_name='authpb.User.roles', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='options', full_name='authpb.User.options', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=177,
)


_PERMISSION = _descriptor.Descriptor(
  name='Permission',
  full_name='authpb.Permission',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='permType', full_name='authpb.Permission.permType', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='key', full_name='authpb.Permission.key', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='range_end', full_name='authpb.Permission.range_end', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PERMISSION_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=180,
  serialized_end=311,
)


_ROLE = _descriptor.Descriptor(
  name='Role',
  full_name='authpb.Role',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='authpb.Role.name', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keyPermission', full_name='authpb.Role.keyPermission', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=313,
  serialized_end=376,
)

_USER.fields_by_name['options'].message_type = _USERADDOPTIONS
_PERMISSION.fields_by_name['permType'].enum_type = _PERMISSION_TYPE
_PERMISSION_TYPE.containing_type = _PERMISSION
_ROLE.fields_by_name['keyPermission'].message_type = _PERMISSION
DESCRIPTOR.message_types_by_name['UserAddOptions'] = _USERADDOPTIONS
DESCRIPTOR.message_types_by_name['User'] = _USER
DESCRIPTOR.message_types_by_name['Permission'] = _PERMISSION
DESCRIPTOR.message_types_by_name['Role'] = _ROLE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserAddOptions = _reflection.GeneratedProtocolMessageType('UserAddOptions', (_message.Message,), {
  'DESCRIPTOR' : _USERADDOPTIONS,
  '__module__' : 'auth_pb2'
  # @@protoc_insertion_point(class_scope:authpb.UserAddOptions)
  })
_sym_db.RegisterMessage(UserAddOptions)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), {
  'DESCRIPTOR' : _USER,
  '__module__' : 'auth_pb2'
  # @@protoc_insertion_point(class_scope:authpb.User)
  })
_sym_db.RegisterMessage(User)

Permission = _reflection.GeneratedProtocolMessageType('Permission', (_message.Message,), {
  'DESCRIPTOR' : _PERMISSION,
  '__module__' : 'auth_pb2'
  # @@protoc_insertion_point(class_scope:authpb.Permission)
  })
_sym_db.RegisterMessage(Permission)

Role = _reflection.GeneratedProtocolMessageType('Role', (_message.Message,), {
  'DESCRIPTOR' : _ROLE,
  '__module__' : 'auth_pb2'
  # @@protoc_insertion_point(class_scope:authpb.Role)
  })
_sym_db.RegisterMessage(Role)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
