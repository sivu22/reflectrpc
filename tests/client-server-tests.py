#!/usr/bin/env python3

from __future__ import unicode_literals
from builtins import bytes, dict, list, int, float, str

import sys
import json
import os
import unittest

sys.path.append('..')

from reflectrpc.client import RpcClient
from reflectrpc.client import RpcError
from reflectrpc.client import NetworkError
from reflectrpc.testing import ServerRunner

class ClientServerTests(unittest.TestCase):
    def test_simple_server(self):
        server = ServerRunner('../examples/server.py', 5500)
        server.run()

        client = RpcClient('localhost', 5500)

        try:
            result = client.rpc_call('echo', 'Hello Server')
            client.close_connection()

            self.assertEqual(result, 'Hello Server')
        finally:
            client.close_connection()
            server.stop()

    def test_twisted_server(self):
        server = ServerRunner('../examples/servertwisted.py', 5500)
        server.run()

        client = RpcClient('localhost', 5500)

        try:
            result = None

            result = client.rpc_call('echo', 'Hello Server')
            client.close_connection()

            self.assertEqual(result, 'Hello Server')
        finally:
            client.close_connection()
            server.stop()

    def test_twisted_server_http(self):
        server = ServerRunner('../examples/serverhttp.py', 5500)
        server.run()

        client = RpcClient('localhost', 5500)
        client.enable_http()

        try:
            result = client.rpc_call('echo', 'Hello Server')

            self.assertEqual(result, 'Hello Server')
        finally:
            client.close_connection()
            server.stop()

    def test_twisted_server_tls(self):
        server = ServerRunner('../examples/servertls.py', 5500)
        server.run()

        client = RpcClient('localhost', 5500)
        client.enable_tls(None, False)

        try:
            result = client.rpc_call('echo', 'Hello Server')

            self.assertEqual(result, 'Hello Server')
        finally:
            client.close_connection()
            server.stop()

    def test_twisted_server_tls_non_tls_client_fail(self):
        server = ServerRunner('../examples/servertls.py', 5500)
        server.run()

        client = RpcClient('localhost', 5500)

        try:

            with self.assertRaises(NetworkError) as cm:
                client.rpc_call('echo', 'Hello Server')

            self.assertEqual(cm.exception.real_exception, "Non-JSON content received")
        finally:
            client.close_connection()
            server.stop()


if __name__ == '__main__':
    unittest.main()
