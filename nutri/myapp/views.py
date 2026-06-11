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

def register_user(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")

        if Login.objects.filter(username=u).exists():
            messages.error(request, "Username already exists")
            return redirect("/register_user")

        l = Login.objects.create_user(
            username=u,
            password=p,
            userType="user",
            viewPass=p
        )

        UserProfile.objects.create(
            loginid=l,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            profile_pic=request.FILES.get("profile_pic")
        )

        messages.success(request, "Registration Successful")
        return redirect("/login")

    return render(request, "user_register.html")

def register_donor(request):
    if request.method == "POST":

        u = request.POST.get("username")
        p = request.POST.get("password")

        if Login.objects.filter(username=u).exists():
            messages.error(request, "Username already exists")
            return redirect("/register_donor")

        l = Login.objects.create_user(
            username=u,
            password=p,
            userType="donor",
            viewPass=p
        )

        DonorProfile.objects.create(
            loginid=l,
            organization_name=request.POST.get("organization_name"),
            donor_type=request.POST.get("donor_type"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            logo=request.FILES.get("logo")
        )

        messages.success(request, "Registration submitted. Wait for admin approval.")
        return redirect("/login")

    return render(request, "donor_register.html")

def register_volunteer(request):
    if request.method == "POST":

        u = request.POST.get("username")
        p = request.POST.get("password")

        if Login.objects.filter(username=u).exists():
            messages.error(request, "Username already exists")
            return redirect("/register_volunteer")

        l = Login.objects.create_user(
            username=u,
            password=p,
            userType="volunteer",
            viewPass=p
        )

        VolunteerProfile.objects.create(
            loginid=l,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            profile_pic=request.FILES.get("profile_pic")
        )

        messages.success(request, "Registration submitted. Wait for admin approval.")
        return redirect("/login")

    return render(request, "volunteer_register.html")


def admin_home(request):
    return render(request, "ADMIN/admin_home.html")

def donor_home(request):
    return render(request, "DONOR/donor_home.html")

def volunteer_home(request):
    return render(request, "VOLUNTEER/volunteer_home.html")

def user_home(request):
    return render(request, "USER/user_home.html")

