# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: courses.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import courses_types_pb2 as courses__types__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rcourses.proto\x1a\x13\x63ourses_types.proto\x1a\x1bgoogle/protobuf/empty.proto2\x9c\x03\n\rCourseService\x12W\n\x10ListCourseTopics\x12 .courses.ListCourseTopicsRequest\x1a!.courses.ListCourseTopicsResponse\x12\x46\n\x0eGetCourseTopic\x12\x1e.courses.GetCourseTopicRequest\x1a\x14.courses.CourseTopic\x12L\n\x11\x43reateCourseTopic\x12!.courses.CreateCourseTopicRequest\x1a\x14.courses.CourseTopic\x12L\n\x11UpdateCourseTopic\x12!.courses.UpdateCourseTopicRequest\x1a\x14.courses.CourseTopic\x12N\n\x11\x44\x65leteCourseTopic\x12!.courses.DeleteCourseTopicRequest\x1a\x16.google.protobuf.Emptyb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'courses_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _COURSESERVICE._serialized_start=68
  _COURSESERVICE._serialized_end=480
# @@protoc_insertion_point(module_scope)
