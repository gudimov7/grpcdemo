"""
Script to generate a protobuf.

Runs protoc with the gRPC plugin to generate messages and gRPC stubs.
"""

from grpc_tools import protoc


if __name__ == '__main__':
    protoc.main((
        '',
        '--python_out=../',
        '--grpc_python_out=../',
        '--pyi_out=../',
        'demo_proto.proto',
    ))
