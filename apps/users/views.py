from sys import int_info

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse
from .forms import LoginUserForm
from django.db.models import Prefetch
from .utils import redirect_with_next, client_ip
import logging
import time

logger = logging.getLogger("users")

def login_view(request):
    ip = client_ip(request)
    start_time = time.perf_counter()
    endpoint = request.get_full_path()
    user_agent = request.META.get("HTTP_USER_AGENT", "")[:200]

    if request.user.is_authenticated:
        return redirect("main:product_list")
    
 
    next_url = request.GET.get("next")
    
    form = LoginUserForm(request=request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = auth.authenticate(request, username=username, password=password)
            

            if not user is None:
                duration = int((time.time() - start_time) * 1000 )

                auth.login(request, user)

                messages.success(request, f"{user.first_name} Ви успішно вішли")

                logger.info(
                    "login_sucsses",
                    extra={
                        "user.id": user.id,
                        "email": user.username,
                        "action": "Login",
                        "status": "success",
                        "method": request.method,
                        "ip": ip,
                        "duration": duration,
                        "endpoint": endpoint,
                        "user_agent": user_agent,
                    }
                )
                return redirect_with_next(request, next_url)
            else:
                logging.warning(
                "login_failed_invalid_credentials",
                extra={
                    "user_id": user.id,
                    "action": "login",
                    "status": "failed",
                    "method": request.method,
                    "ip": ip,
                    "duration": duration,
                    "endpoint": endpoint,
                    "user_agent": user_agent,
                }
                )
        else:
            logger.warning(
                "login_failed_invalid_form",
                extra={
                    "action": "login",
                    "status": "failed",
                    "ip": ip,
                    "errors": form.errors.get_json_data(),
                }
            )
    return render(request, "users/login.html", {"form":form, "next":next_url})


def logout_view(request):
    auth.logout(request)
    return redirect(reverse("main:product_list"))