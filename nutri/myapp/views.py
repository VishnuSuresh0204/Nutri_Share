from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *

# ---------------- LOGIN CHECK ---------------- #

def require_login(request, redirect_url="/login"):
    if "lid" not in request.session:
        messages.error(request, "Please login first")
        return redirect(redirect_url)
    return None

# ---------------- INDEX ---------------- #

def index(request):
    logout(request)
    return render(request, "index.html")

# ---------------- LOGIN ---------------- #

def login_view(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")

        user = authenticate(username=u, password=p)

        if user:
            login(request, user)
            request.session["lid"] = user.id

            if user.userType == "admin":
                return redirect("/admin_home")

            elif user.userType == "donor":
                d = DonorProfile.objects.get(loginid=user)

                if d.status == "approved":
                    return redirect("/donor_home")
                else:
                    messages.error(request, f"Account {d.status}")
                    return redirect("/login")

            elif user.userType == "volunteer":
                v = VolunteerProfile.objects.get(loginid=user)

                if v.status == "approved":
                    return redirect("/volunteer_home")
                else:
                    messages.error(request, f"Account {v.status}")
                    return redirect("/login")

            elif user.userType == "user":
                return redirect("/user_home")

        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("/login")

    return render(request, "login.html")

# ---------------- LOGOUT ---------------- #

def signout(request):
    logout(request)
    return redirect("/")

