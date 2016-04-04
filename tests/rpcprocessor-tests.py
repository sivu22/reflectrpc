#!/usr/bin/env python3

import sys
import json
import unittest

sys.path.append('..')

from reflectrpc import RpcProcessor
from reflectrpc import RpcFunction
from reflectrpc import JsonRpcError

def test_function():
    return True

def echo(msg):
    return msg

def add(a, b):
    return int(a) + int(b)

def echo_array(a):
    return a

def echo_hash(a):
    return a

def internal_error():
    raise ValueError("This should not be visible to the client")

def json_error():
    raise JsonRpcError("User error")

class RpcProcessorTests(unittest.TestCase):
    def test_execute_basic_rpc_request(self):
        rpc = RpcProcessor()

        test_func = RpcFunction(test_function, 'test', 'Returns true',
                'bool', 'Should be true')

        rpc.add_function(test_func)
        reply = rpc.process_request('{"method": "test", "params": [], "id": 1}')
        self.assertEqual(reply['error'], None)
        self.assertTrue(reply['result'])

    def test_echo(self):
        rpc = RpcProcessor()

        echo_func = RpcFunction(echo, 'echo', 'Returns what it was given',
                'string', 'Same value as the first parameter')
        echo_func.add_param('string', 'message', 'Message to send back')

        rpc.add_function(echo_func)
        reply = rpc.process_request('{"method": "echo", "params": ["Hello Server"], "id": 1}')
        self.assertEqual(reply['error'], None)
        self.assertEqual(reply['result'], "Hello Server")

    def test_add(self):
        rpc = RpcProcessor()

        add_func = RpcFunction(add, 'add', 'Returns the sum of two parameters',
                'string', 'Same value as the first parameter')
        add_func.add_param('int', 'a', 'First int to add')
        add_func.add_param('int', 'b', 'Second int to add')

        rpc.add_function(add_func)
        reply = rpc.process_request('{"method": "add", "params": [4, 5], "id": 1}')
        self.assertEqual(reply['error'], None)
        self.assertEqual(reply['result'], 9)

    def test_double_register_of_function(self):
        rpc = RpcProcessor()

        echo_func = RpcFunction(echo, 'echo', 'Returns what it was given',
                'string', 'Same value as the first parameter')
        add_func = RpcFunction(add, 'echo', 'Returns the sum of two parameters',
                'string', 'Same value as the first parameter')

        rpc.add_function(echo_func)
        self.assertRaises(ValueError, rpc.add_function, add_func)

    def test_internal_exception(self):
        rpc = RpcProcessor()

        error_func = RpcFunction(internal_error, 'internal_error', 'Raises ValueError',
                'bool', '')
        rpc.add_function(error_func)

        reply = rpc.process_request('{"method": "internal_error", "params": [], "id": 1}')
        self.assertEqual(reply['error'], {'name': 'InternalError', 'message': 'Internal error'})

    def test_json_exception(self):
        rpc = RpcProcessor()

        error_func = RpcFunction(json_error, 'json_error', 'Raises JsonRpcError',
                'bool', '')
        rpc.add_function(error_func)

        reply = rpc.process_request('{"method": "json_error", "params": [], "id": 1}')
        self.assertEqual(reply['error'], {'name': 'JsonRpcError', 'message': 'User error'})

    def test_wrong_number_of_params(self):
        rpc = RpcProcessor()

        echo_func = RpcFunction(echo, 'echo', 'Returns what it was given',
                'string', 'Same value as the first parameter')
        echo_func.add_param('string', 'message', 'Message to send back')

        rpc.add_function(echo_func)

        reply = rpc.process_request('{"method": "echo", "params": ["Hello Server", 42], "id": 1}')
        self.assertEqual(reply['error'], {'name': 'ParamError', 'message': 'Expected 1 parameters for \'echo\' but got 2'})

        reply = rpc.process_request('{"method": "echo", "params": [], "id": 2}')
        self.assertEqual(reply['error'], {'name': 'ParamError', 'message': 'Expected 1 parameters for \'echo\' but got 0'})

    def test_type_checks(self):
        rpc = RpcProcessor()

        echo_func = RpcFunction(echo, 'echo', 'Returns what it was given',
                'string', 'Same value as the first parameter')
        echo_func.add_param('string', 'message', 'Message to send back')

        rpc.add_function(echo_func)

        add_func = RpcFunction(add, 'add', 'Returns the sum of two parameters',
                'string', 'Same value as the first parameter')
        add_func.add_param('int', 'a', 'First int to add')
        add_func.add_param('int', 'b', 'Second int to add')

        rpc.add_function(add_func)

        reply = rpc.process_request('{"method": "echo", "params": [42], "id": 1}')
        self.assertEqual(reply['error'], {'name': 'TypeError', 'message':'echo: Expected value of type \'string\' for parameter \'message\' but got value of type \'int\''})

        reply = rpc.process_request('{"method": "echo", "params": [[]], "id": 2}')
        self.assertEqual(reply['error'], {'name': 'TypeError', 'message':'echo: Expected value of type \'string\' for parameter \'message\' but got value of type \'array\''})

        reply = rpc.process_request('{"method": "add", "params": [4, 8.9], "id": 3}')
        self.assertEqual(reply['error'], {'name': 'TypeError', 'message':'add: Expected value of type \'int\' for parameter \'b\' but got value of type \'float\''})

        reply = rpc.process_request('{"method": "add", "params": [4, {"test": 8}], "id": 3}')
        self.assertEqual(reply['error'], {'name': 'TypeError', 'message':'add: Expected value of type \'int\' for parameter \'b\' but got value of type \'hash\''})


if __name__ == '__main__':
    unittest.main()
