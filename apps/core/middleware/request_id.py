from contextvars import ContextVar

_request_id_var = ContextVar("request_id", default=None)

def get_request_id():
    return _request_id_var.get()

def set_request_id(request):
    _request_id_var.set(request)