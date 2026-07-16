import uuid
from .request_id import set_request_id


class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        set_request_id(request_id)
        request.request_id = request_id

        response = self.get_response(request)

        response["X-Request-ID"] = request_id

        return response