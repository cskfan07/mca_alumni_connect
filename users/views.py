from django.shortcuts import render, redirect
from django.conf import settings
from users.mongo import init_mongo
from django.contrib.auth.hashers import check_password, make_password
from functools import wraps
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Enquiry, Notification
from .models import JobPost,Profile
from django.contrib import messages
from .models import MentorshipRequest, PrivateChat
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from urllib.parse import quote
import secrets

token_generator = PasswordResetTokenGenerator()
def home(request):
    return render(request, 'landing.html')
# =============================
# Custom Login Required Decorator
# =============================
def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper
# =============================
# Register New User
# =============================
@csrf_exempt
def register_user(request):

    if request.method == 'GET':
        return render(request, 'register.html')

    elif request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        roll_no = data.get('roll_no')
        reg_no = data.get('reg_no')
        passoutyear = data.get('endyear')

        if not roll_no or not reg_no or not passoutyear:
            return JsonResponse({'error': 'Roll No, Reg No, and Passout Year are required!'}, status=400)

        if not username or not email or not password:
            return JsonResponse({'error': 'All fields required'}, status=400)

        if User.objects(email=email).first():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        hashed_password = make_password(password)
        token = secrets.token_urlsafe(16)

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role,
            is_Verified=0,
            is_Active=False,
            email_token=token,
            roll_no=roll_no,
            reg_no=reg_no,
            passout_Year=passoutyear
        )
        user.save()

        email_encoded = quote(email)
        verify_link = (
            f"https://mca-alumni-connect.onrender.com/"
            f"verify-email/{email_encoded}/{token}/"
        )

        try:
            send_mail(
                "Verify your email",
                f"Click this link to verify your email:\n{verify_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({
            'message': 'Registration successful! Check your email to verify.'
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)


from urllib.parse import unquote

def verify_email(request, email, token):
    email = unquote(email)

    user = User.objects(email=email, email_token=token).first()
    if not user:
        return HttpResponse("Invalid verification link")

    user.is_Verified = 2
    user.email_token = ""
    user.save()

    return HttpResponse("Email verified! You can now wait for admin approval.")
# =============================
# Login User
# =============================

@csrf_exempt
def login_user(request):
  

    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        # 🔥 JSON vs FORM support
        if request.content_type == "application/json":
            import json
            data = json.loads(request.body)
        else:
            data = request.POST

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({'error': 'Email and password required'}, status=400)

        user = User.objects(email=email).first()
        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)

        if not check_password(password, user.password):
            return JsonResponse({'error': 'Incorrect password!'}, status=400)

        if user.is_Verified != 1:
            if user.is_Verified == 0:
                return JsonResponse({"error": "Please verify your email first"}, status=403)
            if user.is_Verified == 2:
                return JsonResponse({"error": "Waiting for admin approval"}, status=403)
            if user.is_Verified == -1:
                return JsonResponse({"error": "Your account was rejected"}, status=403)

        user.is_Active = True
        user.save()

        # Save session
        request.session['user_id'] = str(user.id)
        request.session['username'] = user.username
        request.session['role'] = user.role

        # Role Based Redirect
        if user.role == "admin":
            return JsonResponse({'redirect': '/roles/admin_panel/'})
        elif user.role == "student":
            return JsonResponse({'redirect': '/roles/student_dash/'})
        elif user.role == "alumni":
            return JsonResponse({'redirect': '/roles/alumni_dash/'})

        return JsonResponse({'redirect': '/dashboard/'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)
# =============================
# Logout User
# =============================
def logout_user(request):
   
    user_id = request.session.get("user_id")

    if user_id:
        user = User.objects(id=user_id).first()
        if user:
            user.is_Active = False      # EXACT correct field name
            user.save()

    request.session.flush()  # clear session
    return redirect("home")
# =============================
# Default Dashboard
# =============================
@login_required_custom
def dashboard(request):
  
    role = request.session.get("role")

    if role == "admin":
        return redirect("/roles/admin_panel/")
    elif role == "student":
        return redirect("/roles/student_dash/")
    elif role == "alumni":
        return redirect("/roles/alumni_dash/")

    return redirect("/login/")

# =============================
# Role Based Dashboards
# =============================
@login_required_custom
def admin_panel(request):
 
    if request.session.get('role') != 'admin':
        return redirect('/dashboard/')

    from .models import User,Profile
    from collections import defaultdict


    # ---------- Fetch Logged-in Admin ----------
    admin_id = request.session.get('user_id')
    logged_user = User.objects.get(id=admin_id)
    profile = Profile.objects(user=logged_user).first()
    job_posts = JobPost.objects.all()
    all_profile= Profile.objects.all()

    # New list with user details
    jobp = []

    for job in job_posts:
        user = User.objects(id=job.user_id).first()

        jobp.append({
            "id": str(job.id),
            "title": job.title,
            "company": job.company,
            "type": job.type,
            "description": job.description,
            "link": job.link,
            "expiry": job.expiry,
            "post_status": job.post_status,

            # USER COLLECTION SE DATA
            "username": user.username if user else "Unknown",
            "role": user.role if user else "Unknown",
        })

    # ---------- Daily Graph Data (Trend Chart) ----------
    users = User.objects.only('role', 'created_on')

    student_day = defaultdict(int)
    alumni_day = defaultdict(int)
    admin_day = defaultdict(int)

    for u in users:
        if not u.created_on:
            continue

        day = u.created_on.strftime("%Y-%m-%d")

        if u.role == "student":
            student_day[day] += 1
        elif u.role == "alumni":
            alumni_day[day] += 1
        elif u.role == "admin":
            admin_day[day] += 1

    days = sorted(set(list(student_day) + list(alumni_day) + list(admin_day)))

    student_counts = [student_day[d] for d in days]
    alumni_counts = [alumni_day[d] for d in days]
    admin_counts = [admin_day[d] for d in days]

    alluser=User.objects.all()

    # ---------- Dashboard Counts ----------
    pending_users = User.objects(is_Verified=0 )
    e_v_pending_users= User.objects(is_Verified=2)
    e_v_count=e_v_pending_users.count()
    pending_count = pending_users.count() + e_v_count
    verified_users = User.objects(is_Verified=1).count()
    v_user=User.objects(is_Verified=1)
    rejected_users = User.objects(is_Verified=-1).count()
    total_users = User.objects.count()

    n_alm = User.objects(role="alumni", is_Verified=1).count()
    n_adm = User.objects(role="admin", is_Verified=1).count()
    n_std = User.objects(role="student", is_Verified=1).count()

    enq_data = Enquiry.objects()
    enq_count=Enquiry.objects().count()

    posts = JobPost.objects.only('created_at')

    post_day = defaultdict(int)

    for post in posts:
        if post.created_at:
            day = post.created_at.strftime("%Y-%m-%d")
            post_day[day] += 1

    # sort dates
    days = sorted(post_day.keys())
    post_counts = [post_day[d] for d in days]


    return render(request, "roles/admin_panel.html", {
        "pending_users": e_v_pending_users,
        "pending_count": pending_count,
        "verified_user": verified_users,
        "reject_user": rejected_users,
        "total_user": total_users,
        "v_user":v_user,
        "no_alm": n_alm,
        "no_adm": n_adm,
        "no_std": n_std,

        # Trend Graph Data
        "days": json.dumps(days),
        "student_counts": json.dumps(student_counts),
        "alumni_counts": json.dumps(alumni_counts),
        "admin_counts": json.dumps(admin_counts),
        "post_days": json.dumps(days),
        "post_counts": json.dumps(post_counts),

        # Logged-in Admin Data
        "logged_user": logged_user,
        "profile": profile,
        #total enqiury data and num, of data
        "enq_data": enq_data,
        "no_fq":enq_count,
    #     job post view in admin panle
        "jobpost":jobp,
        "alluser":alluser,
        "allprofile":all_profile,
    })
@login_required_custom
@csrf_exempt
def update_user_status(request):
 
    # Only admin can do this
    if request.session.get('role') != 'admin':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get('user_id')       # ID of the user to update
        approve = data.get('approve')

        if not user_id:
            return JsonResponse({'error': 'User ID missing'}, status=400)

        # Fetch user from MongoDB
        try:
            updated = User.objects(id=user_id).update(is_Verified=approve)
            if updated == 0:
                return JsonResponse({'error': 'User not found'}, status=404)

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
# ///////////////////////////////////////
 #   enquiry form
 # /////////////////////////////////////////////
@csrf_exempt
def enq(request):
   
    if request.method == 'POST':
        data = json.loads(request.body)
        print("📌 Received Data:", data)

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not name or not email or not message:
            return JsonResponse({'error': 'All fields required'}, status=400)

        try:
            Enquiry(
                name=name,
                email=email,
                message=message,
                time=datetime.now()
            ).save()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'message': 'sent successful! :)'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def load_admin_page(request, page):
    try:
        return render(request, f"roles/admin_menu/{page}.html")
    except:
        return HttpResponse("Page not found", status=404)


# here we crete an function that take data from collection enquiry

def jobpost(request):
     
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            title = data.get("title")
            type_ = data.get("type")
            company = data.get("company")
            description = data.get("description")
            link = data.get("link")
            posted_by = data.get("posted_by")
            expiry = data.get("expiry")

            # Convert expiry date
            if expiry:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
            else:
                expiry_date = None

            # 🟢 SAVE IN MONGO ENGINE
            job = JobPost(
                title=title,
                type=type_,
                company=company,
                description=description,
                link=link,
                user_id=posted_by,
                expiry=expiry_date
            )
            job.save()

            return JsonResponse({"message": "Post Published Successfully!"})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"message": "Error: " + str(e)}, status=500)

    return JsonResponse({"message": "Invalid Request"}, status=400)

# admin profile save krne ke liy
@login_required_custom
@csrf_exempt
def save_profile(request):
   
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("/login/")

        user = User.objects.get(id=user_id)

        # Get existing profile or create new
        profile = Profile.objects(user=user).first()
        if not profile:
            profile = Profile(user=user)

        # Update fields
        profile.curnt_wrk_role = request.POST.get("cwr")
        profile.dob = request.POST.get("dob")
        profile.age = request.POST.get("age")
        profile.skill = request.POST.get("skill")
        profile.cwc = request.POST.get("cwc")
        profile.loc = request.POST.get("loc")
        profile.ph = request.POST.get("ph")
        profile.wexp = request.POST.get("wexp")
        profile.llink = request.POST.get("llink")
        profile.bio = request.POST.get("bio")

        # Handle photo
        if request.FILES.get("photo"):
            file_obj = request.FILES["photo"]
            if profile.photo:
                profile.photo.replace(file_obj, content_type=file_obj.content_type)
            else:
                profile.photo.put(file_obj, content_type=file_obj.content_type)

        profile.save()
        messages.success(request, "Profile saved successfully!")

        # Redirect to admin panel (or render with updated profile)
        return redirect("/roles/admin_panel/?open=profile_menu")

    return redirect("/roles/admin_panel/")

def serve_profile_photo(request, profile_id):
   
    try:
        profile = Profile.objects.get(id=profile_id)
        if profile.photo:
            response = HttpResponse(profile.photo.read(), content_type=profile.photo.content_type)
            return response
    except Profile.DoesNotExist:
        pass
    return HttpResponse(status=404)

@csrf_exempt
@login_required_custom
def update_job_status(request):
 
    if request.method == "POST":
        data = json.loads(request.body)
        job_id = data.get("job_id")
        status = data.get("status")   # 1 approve, -1 reject

        if not job_id:
            return JsonResponse({"error": "Job ID missing"}, status=400)

        try:
            job = JobPost.objects.get(id=job_id)
            job.post_status = status
            job.save()

            # 🔔 NOTIFICATION WHEN APPROVED
            if status == 1:
                users = User.objects(
                    role__in=["student", "alumni"],
                    is_Verified=1,
                    is_Active=True
                )

                for user in users:
                    Notification(
                        user=user,
                        message=f"New Job Approved: {job.title} at {job.company}"
                    ).save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
@login_required_custom
def student_dash(request):
  
    if request.session.get('role') != 'student':
        return redirect('/dashboard/')

    student_id = request.session.get('user_id')
    logged_user_s = User.objects.get(id=student_id)
    student_profile = Profile.objects(user=logged_user_s).first()

    alumni_users = User.objects(role="alumni", is_Verified=1)
    alumni_profiles = Profile.objects(user__in=alumni_users)

    today = datetime.now()

    jobs = JobPost.objects(post_status=1, expiry__gte=today).order_by('expiry')

    #   GET POSTED-BY USER NAME --------
    job_list = []
    for job in jobs:
        posted_by_user = User.objects(id=job.user_id).first()

        job_list.append({
             "id": str(job.id),
            "title": job.title,
            "description": job.description,
            "type": job.type,
            "company": job.company,
            "link": job.link,
            "expiry": job.expiry,
            "posted_by": posted_by_user.username if posted_by_user else "Unknown",
            "posted_by_user": posted_by_user,
            "role":posted_by_user.role
        })
    # -----------------------------------------------------------------

    # -------------------- Alumni + Mentorship Status -----------------
    alumni = []

    for user in alumni_users:
        profile = next((p for p in alumni_profiles if p.user.id == user.id), None)

        req = MentorshipRequest.objects(
            student=logged_user_s,
            alumni=user
        ).first()

        alumni.append({
            "user": user,
            "profile": profile,
            "requested": True if req else False,
            "accepted": True if req and req.status == "accepted" else False,
            "chat_id": str(req.id) if req and req.status == "accepted" else ""
        })
    notifications = Notification.objects(user=logged_user_s).order_by('-created_at')[:10]
    unread_count = Notification.objects(user=logged_user_s, is_read=False).count()

    # Get active mentorships where status is 'accepted'
    active_mentorships = MentorshipRequest.objects(
        student=logged_user_s,
        status='accepted'
    )
    private_chats = []
    for mentorship in active_mentorships:
        msgs = PrivateChat.objects(mentorship_id=mentorship.id).order_by('timestamp')
        private_chats.append({
            "mentorship": mentorship,
            "messages": msgs
        })

    return render(request, "roles/student_dash.html", {
        "stdt": logged_user_s,
        "sprfl": student_profile,
        "alumni": alumni,
        "jobi": job_list,
        "pchat": private_chats,
        "notifications": notifications,
        "unread_count": unread_count,
    })
def send_mentorship_request(request, alumni_id):
   
    if request.session.get('role') != 'student':
        return redirect('/dashboard/')

    student_id = request.session.get('user_id')

    student = User.objects.get(id=student_id)
    alumni = User.objects.get(id=alumni_id)

    # Check if already sent
    if MentorshipRequest.objects(student=student, alumni=alumni).first():
        messages.warning(request, "You already sent a request to this alumni.")
        return redirect('/roles/student_dash/')

    # Create new request
    MentorshipRequest(
        student=student,
        alumni=alumni,
        message="I would like mentorship from you."
    ).save()

    messages.success(request, "Mentorship request sent successfully!")
    return redirect('/roles/student_dash/')

@login_required_custom
def alumni_dash(request):
   
    if request.session.get('role') != 'alumni':
        return redirect('/dashboard/')

    alumni_id = request.session.get('user_id')
    alumni_user = User.objects.get(id=alumni_id)
    alumni_profile = Profile.objects(user=alumni_user).first()

    # 🔹 Mentorship requests (already present)
    requests = MentorshipRequest.objects(alumni=alumni_user).order_by('-created_at')

    req_list = []
    for req in requests:
        student = req.student
        student_profile = Profile.objects(user=student).first()

        req_list.append({
            "id": str(req.id),
            "student": student,
            "profile": student_profile,
            "message": req.message,
            "status": req.status,
            "created_at": req.created_at
        })

    #  STATS
    total_requests = len(req_list)
    pending_count = len([r for r in req_list if r["status"] == "pending"])
    accepted_count = len([r for r in req_list if r["status"] == "accepted"])

    jobs = JobPost.objects(user_id=str(alumni_user.id)).order_by('-expiry')

    job_list = []
    for job in jobs:
        job_list.append({
            "id": str(job.id),
            "title": job.title,
            "type": job.type,
            "company": job.company,
            "description": job.description,
            "link": job.link,
            "expiry": job.expiry,
            "post_status": job.post_status,
        })

    return render(request, "roles/alumni_dash.html", {
        "stdt": alumni_user,
        "sprfl": alumni_profile,

        # mentorship data
        "requests": req_list,
        "total_requests": total_requests,
        "pending_count": pending_count,
        "accepted_count": accepted_count,

        "jobi": job_list,
    })
@login_required_custom
def load_alumni_page(request, page):
    
    if request.session.get('role') != 'alumni':
        return redirect('/dashboard/')

    try:
        return render(request, f"roles/alumni_menu/{page}.html")
    except:
        return HttpResponse("Page not found", status=404)

@login_required_custom
@csrf_exempt
def update_mentorship_status(request):
    
   
    if request.session.get('role') != 'alumni':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == "POST":
        data = json.loads(request.body)
        req_id = data.get("request_id")
        status = data.get("status")  # accepted / rejected

        req = MentorshipRequest.objects(id=req_id).first()
        if not req:
            return JsonResponse({'error': 'Request not found'}, status=404)

        req.status = status
        req.save()

        # 🔔 NOTIFICATION ON ACCEPT
        if status == "accepted":
            Notification(
                user=req.student,
                message=f"Your mentorship request was accepted by {req.alumni.username}"
            ).save()

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_notifications(user):
  
    return Notification.objects(user=user).order_by('-created_at')

def unread_notification_count(user):
 
    return Notification.objects(user=user, is_read=False).count()


@login_required_custom
def student_chat(request, mentorship_id):
  
    if request.session.get("role") != "student":
        return redirect("/dashboard/")

    student_id = request.session.get("user_id")
    student = User.objects.get(id=student_id)

    mentorship = MentorshipRequest.objects(id=mentorship_id).first()
    if not mentorship or mentorship.student != student:
        return HttpResponse("Unauthorized", status=403)

    messages = PrivateChat.objects(
        mentorship_id=mentorship.id
    ).order_by("timestamp")

    return render(request, "roles/student_menu/chat_std_menu.html", {
        "mentorship": mentorship,
        "messages": messages
    })

@login_required_custom
def private_chat(request, mentorship_id):
  
    # Fetch mentorship request
    mentorship = MentorshipRequest.objects.get(id=mentorship_id)

    user_id = request.session.get("user_id")
    logged_user = User.objects.get(id=user_id)

    # Only allow student or alumni involved to see the chat
    if logged_user.id not in [mentorship.student.id, mentorship.alumni.id]:
        return redirect('/dashboard/')

    # Fetch all messages
    messages = PrivateChat.objects(mentorship_id=mentorship).order_by('timestamp')

    # Determine chat partner
    if logged_user.id == mentorship.student.id:
        chat_partner = mentorship.alumni
    else:
        chat_partner = mentorship.student

    return render(request, "roles/student_menu/chat_std_menu.html", {
        "mentorship": mentorship,
        "messages": messages,
        "chat_partner": chat_partner,
        "logged_user": logged_user,
    })

@csrf_exempt
@login_required_custom
def send_private_message(request, mentorship_id):
  
    if request.method == "POST":
        data = json.loads(request.body)
        msg_text = data.get("message")

        mentorship = MentorshipRequest.objects.get(id=mentorship_id)
        user_id = request.session.get("user_id")
        sender = User.objects.get(id=user_id)

        # Only student or alumni can send
        if sender.id not in [mentorship.student.id, mentorship.alumni.id]:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        # Save message
        PrivateChat(
            mentorship_id=mentorship,
            student_id=mentorship.student,
            alumni_id=mentorship.alumni,
            sender_id=sender,
            message=msg_text
        ).save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=405)
