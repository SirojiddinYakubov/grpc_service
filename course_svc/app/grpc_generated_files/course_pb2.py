# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: course.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x63ourse.proto\x12\x06\x63ourse\x1a\x1egoogle/protobuf/wrappers.proto\"\'\n\x12\x43heckCourseRequest\x12\x11\n\tcourse_id\x18\x01 \x01(\t2W\n\rCourseService\x12\x46\n\x0c\x63heck_course\x12\x1a.course.CheckCourseRequest\x1a\x1a.google.protobuf.BoolValueb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'course_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CHECKCOURSEREQUEST._serialized_start=56
  _CHECKCOURSEREQUEST._serialized_end=95
  _COURSESERVICE._serialized_start=97
  _COURSESERVICE._serialized_end=184
# @@protoc_insertion_point(module_scope)
