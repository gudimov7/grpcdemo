"""Main entry point."""
import logging
import os

import grpc
from concurrent import futures

import demo_proto_pb2_grpc
from services import GrpcService

logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',  # Define log template
    datefmt='%m-%d %H:%M',  # Set date/time format
    # filename='myapp.log',  # Optional: Log to a file
    # filemode='w'  # Optional: Overwrite existing file
)

with open('cert/server.key', 'rb') as f:
    private_key = f.read()
with open('cert/server.pem', 'rb') as f:
    certificate_chain = f.read()

credentials = grpc.ssl_server_credentials([(private_key, certificate_chain)])


def serve(ssl_port: int, port: int = 50051) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # server.credentials = credentials
    server.add_insecure_port(f'[::]:{port}')  # For local testing without SSL
    server.add_secure_port(f'[::]:{ssl_port}', credentials)  # For production with SSL

    demo_proto_pb2_grpc.add_grpc_serviceServicer_to_server(GrpcService(), server)

    server.start()

    try:
        logging.info(f"Server started")
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    if not os.path.exists("demo_proto_pb2_grpc.py") or not os.path.exists("demo_proto_pb2.py"):
        os.system("python protos/generate_proto.py")

    ssl_port = 51051
    port = 50051
    serve(ssl_port=ssl_port, port=port)
