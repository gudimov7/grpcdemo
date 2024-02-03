# Grpc Demo server with TLC security

## Table of Contents

- [Pre installations](#pre-installations)
- [Project Structure](#project-structure)
- [Running](#running)
- [Main Implementation](#main-method-implementation)

## Pre Installations

- ### Install Python
  - For windows
  ```bash
     python3
  ```
  - For Linux
  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo apt install python3 python3-dev libpython3-dev python3-tools
  ```
- ### Install Poetry from: [documentation](https://python-poetry.org/docs/#installing-with-the-official-installer)
  - For windows
  ```bash
     (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
  ```
  - For Linux
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```
  - Add Poetry to PATH environment variable
- ### Install dependencies
  - I'm using Poetry to mange project dependencies
  - and all dependencies are in pyproject.toml file
  - In order to get all dependencies used by this project run
    ```bash
    poetry install
    ```
    from command line, this will install all project dependecies, and will allow you to run this project smoothly.
- Create TLC certificates
  - Go to Project RootFolder/cert in your command line
  - and run to create TLC certificates for your server:
  ```bash
  openssl req -newkey rsa:4096 -nodes -keyout key.pem -x509 -days 365 -out cert.pem cat cert.pem > chain.pem
  ```

## Project Structure

    Root (Project Root)
        | cert (Project TLC certificates)
        | protos (gRPC proto files) # including script to generate protobuff files
        | services (gRPC endpoints implimentations)
        pyproject.toml (Project managment file, including dependencies)
        main.py (Project main entry point)

## Running

From Root folder (Make sure certificates created before running ssl server)
You can comment out lines 19-24 and 31 in main.py to run grpc server without TLC, make sure to send requests without TLC

```bash
poetry install --no-root
poetry run python main.py
```

## Main method implementation

```python
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
    serve(ssl_port=ssl_port, port=port)if __name__ == '__main__':
    ssl_port = 51051
    port = 50051
    serve(ssl_port=ssl_port, port=port)

```
