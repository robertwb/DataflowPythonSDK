# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for the pickler module."""

import unittest

from google.cloud.dataflow.internal import module_test
from google.cloud.dataflow.internal.pickler import dumps
from google.cloud.dataflow.internal.pickler import loads


class PicklerTest(unittest.TestCase):

  def test_basics(self):
    self.assertEquals([1, 'a', (u'z',)], loads(dumps([1, 'a', (u'z',)])))
    fun = lambda x: 'xyz-%s' % x
    self.assertEquals('xyz-abc', loads(dumps(fun))('abc'))

  def test_lambda_with_globals(self):
    """Tests that the globals of a function are preserved."""

    # The point of the test is that the lambda being called after unpickling
    # relies on having the re module being loaded.
    self.assertEquals(
        ['abc', 'def'],
        loads(dumps(module_test.get_lambda_with_globals()))('abc def'))

  def test_lambda_with_closure(self):
    """Tests that the closure of a function is preserved."""
    self.assertEquals(
        'closure: abc',
        loads(dumps(module_test.get_lambda_with_closure('abc')))())

  def test_class(self):
    """Tests that a class object is pickled correctly."""
    self.assertEquals(
        ['abc', 'def'],
        loads(dumps(module_test.Xyz))().foo('abc def'))

  def test_object(self):
    """Tests that a class instance is pickled correctly."""
    self.assertEquals(
        ['abc', 'def'],
        loads(dumps(module_test.XYZ_OBJECT)).foo('abc def'))

  def test_nested_class(self):
    """Tests that a nested class object is pickled correctly."""
    self.assertEquals(
        'X:abc',
        loads(dumps(module_test.TopClass.NestedClass('abc'))).datum)
    self.assertEquals(
        'Y:abc',
        loads(dumps(module_test.TopClass.MiddleClass.NestedClass('abc'))).datum)

  def test_dynamic_class(self):
    """Tests that a nested class object is pickled correctly."""
    self.assertEquals(
        'Z:abc',
        loads(dumps(module_test.create_class('abc'))).get())

  def test_generators(self):
    with self.assertRaises(TypeError):
      dumps((_ for _ in range(10)))

if __name__ == '__main__':
  unittest.main()
