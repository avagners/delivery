import grpc
from config import GEO_SERVICE
from core.ports.location_provider import LocationProvider
from core.domain.model.shared_kernel.location import Location
from infrastructure.adapters.grpc.geo_service import geo_pb2, geo_pb2_grpc


class GeoClient(LocationProvider):
    def __init__(self, address=GEO_SERVICE):
        self.channel = grpc.insecure_channel(address)
        self.stub = geo_pb2_grpc.GeoStub(self.channel)

    def get_location_by_street(self, street: str) -> Location:
        request = geo_pb2.GetGeolocationRequest(Street=street)
        response = self.stub.GetGeolocation(request)

        return Location(
            x=response.Location.x,
            y=response.Location.y
        )
