from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect, resolve_url


def redirect_with_next(request, next_url=None, default="main:product_list"):
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host(), require_https=request.is_secure()):
        return redirect(next_url)
    return redirect(resolve_url(default))

def client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].split()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip 