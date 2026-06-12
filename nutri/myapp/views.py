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


def admin_view_donors(request):
    d = DonorProfile.objects.all()
    return render(request, "ADMIN/view_donors.html", {"val": d})

def admin_donor_action(request):
    id = request.GET.get("id")
    act = request.GET.get("act")

    d = DonorProfile.objects.get(id=id)
    d.status = act
    d.save()

    return redirect("/admin_view_donors")

def admin_view_volunteers(request):
    v = VolunteerProfile.objects.all()
    return render(request, "ADMIN/view_volunteers.html", {"val": v})


def admin_volunteer_action(request):
    id = request.GET.get("id")
    act = request.GET.get("act")

    v = VolunteerProfile.objects.get(id=id)
    v.status = act
    v.save()

    return redirect("/admin_view_volunteers")

def admin_view_users(request):
    u = UserProfile.objects.all()
    return render(request, "ADMIN/view_users.html", {"val": u})

def admin_view_complaints(request):
    c = Complaint.objects.all().order_by("-created_at")
    return render(request, "ADMIN/view_complaints.html", {"val": c})


def admin_reply_complaint(request):
    id = request.GET.get("id")

    c = Complaint.objects.get(id=id)

    if request.method == "POST":
        c.reply = request.POST.get("reply")
        c.status = "replied"
        c.save()

        return redirect("/admin_view_complaints")

    return render(request, "ADMIN/reply_complaint.html", {"c": c})

def admin_view_feedback(request):
    f = Feedback.objects.all().order_by("-created_at")
    return render(request, "ADMIN/view_feedback.html", {"val": f})



def donor_home(request):
    return render(request, "DONOR/donor_home.html")


def donor_add_donation(request):

    donor = DonorProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    if request.method == "POST":

        FoodDonation.objects.create(
            donor=donor,
            food_name=request.POST.get("food_name"),
            food_type=request.POST.get("food_type"),
            quantity=request.POST.get("quantity"),
            description=request.POST.get("description"),
            expiry_time=request.POST.get("expiry_time"),
            pickup_address=request.POST.get("pickup_address")
        )

        messages.success(request, "Donation Added")
        return redirect("/donor_view_donations")

    return render(request, "DONOR/add_donation.html")


def donor_add_donation(request):

    donor = DonorProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    if request.method == "POST":

        FoodDonation.objects.create(
            donor=donor,
            food_name=request.POST.get("food_name"),
            food_type=request.POST.get("food_type"),
            quantity=request.POST.get("quantity"),
            description=request.POST.get("description"),
            expiry_time=request.POST.get("expiry_time"),
            pickup_address=request.POST.get("pickup_address")
        )

        messages.success(request, "Donation Added")
        return redirect("/donor_view_donations")

    return render(request, "DONOR/add_donation.html")

def donor_view_donations(request):

    donor = DonorProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    d = FoodDonation.objects.filter(donor=donor)

    return render(request,
                  "DONOR/view_donations.html",
                  {"val": d})

def donor_delete_donation(request):
    id = request.GET.get("id")

    FoodDonation.objects.filter(id=id).delete()

    return redirect("/donor_view_donations")
def donor_donation_history(request):

    donor = DonorProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    d = FoodDonation.objects.filter(
        donor=donor
    ).order_by("-donation_date")

    return render(request,
                  "DONOR/donation_history.html",
                  {"val": d})



def volunteer_home(request):
    return render(request, "VOLUNTEER/volunteer_home.html")


def volunteer_view_tasks(request):

    v = VolunteerProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    tasks = VolunteerAssignment.objects.filter(
        volunteer=v
    )

    return render(request,
                  "VOLUNTEER/view_tasks.html",
                  {"val": tasks})

def volunteer_accept_task(request):

    id = request.GET.get("id")

    a = VolunteerAssignment.objects.get(id=id)

    a.accepted = True
    a.save()

    return redirect("/volunteer_view_tasks")

def volunteer_reject_task(request):

    id = request.GET.get("id")

    a = VolunteerAssignment.objects.get(id=id)

    a.accepted = False
    a.save()

    return redirect("/volunteer_view_tasks")

def volunteer_update_status(request):

    id = request.GET.get("id")
    st = request.GET.get("status")

    a = VolunteerAssignment.objects.get(id=id)

    a.pickup_status = st
    a.save()

    return redirect("/volunteer_view_tasks")



def user_home(request):
    return render(request, "USER/user_home.html")


def user_view_donations(request):

    d = FoodDonation.objects.filter(
        status="available"
    )

    return render(request,
                  "USER/view_donations.html",
                  {"val": d})

def user_request_food(request):

    did = request.GET.get("did")

    user = UserProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    donation = FoodDonation.objects.get(id=did)

    FoodRequest.objects.create(
        user=user,
        donation=donation
    )

    messages.success(request, "Request Sent")

    return redirect("/user_view_requests")

def user_request_food(request):

    did = request.GET.get("did")

    user = UserProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    donation = FoodDonation.objects.get(id=did)

    FoodRequest.objects.create(
        user=user,
        donation=donation
    )

    messages.success(request, "Request Sent")

    return redirect("/user_view_requests")

def user_add_feedback(request):

    user = UserProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    if request.method == "POST":

        Feedback.objects.create(
            user=user,
            rating=request.POST.get("rating"),
            message=request.POST.get("message")
        )

        return redirect("/user_view_feedback")

    return render(request, "USER/add_feedback.html")

def user_view_feedback(request):

    user = UserProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    f = Feedback.objects.filter(user=user)

    return render(request,
                  "USER/view_feedback.html",
                  {"val": f})

def user_add_complaint(request):

    user = UserProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    if request.method == "POST":

        Complaint.objects.create(
            user=user,
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )

        return redirect("/user_view_complaints")

    return render(request, "USER/add_complaint.html")


