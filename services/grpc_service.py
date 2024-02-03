"""GrpcService definition."""
import logging

import demo_proto_pb2_grpc
from demo_proto_pb2 import BaseResponse

class GrpcService(demo_proto_pb2_grpc.grpc_serviceServicer):
    """GrpcService definition."""

    def __init__(self):
        self.response_id_counter = 0

    def Ack(self, request, context):
        """SayHello empty request."""
        logging.info("received request: %s", request)
        return self._response(request, "ok")

    def SendData(self, request, context):
        """SendGrades full request."""
        logging.info("request name: %s", request.Name)
        logging.info("request age: %s", request.Age)
        logging.info("request grades: %s", [f"{grade} ," for grade in request.ListGrades])
        return self._response(request, "ok")

    def _response(self, request, msg):
        """Private response creator."""
        self.response_id_counter += 1
        return BaseResponse(ResponseId=self.response_id_counter,
                            RequestId=request.RequestId,
                            Message=msg)
