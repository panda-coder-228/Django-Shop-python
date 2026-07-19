from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse
from .forms import LoginUserForm, UserRegistrationForm, UserProfileForm
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
    
    # безопасний redirect for login_required
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

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect(reverse("main:product_list"))


def registration(request):
    print(request.method)
    if request.user.is_authenticated:
        return redirect("main:product_list")
    
    
    form = UserRegistrationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, f"{user.first_name} Ви успішно зареєструвались!")
            logging.info(
                "Registration_success",
                extra={
                    "email": request.user.email,
                    "action": "Registration",
                    "method": request.method,
                    "status": "success",
                }
            )
            return redirect("main:product_list")
        else:
            logger.warning(
                "Registration_failed_invalied_form",
                extra={
                    "email": form.data.get("email"),
                    "status": "failed",
                    "action": "Registartion",
                }
            )
    return render(request, "users/registration.html", {'form':form})

@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"{user.first_name} Профіль успішно оновлено!"
            )
            return redirect("users:profile")

        logger.warning(
            "Profile update failed: invalid form",
            extra={
                "user": request.user.email,
                "action": "profile_update",
                "status": "failed",
                "method": request.method,
                "errors": form.errors.get_json_data(),
            },
        )

    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form})