from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Role Based Dashboards
    path('roles/admin_panel/', views.admin_panel, name='admin_panel'),
    path('roles/student_dash/', views.student_dash, name='student_dash'),
    path('roles/alumni_dash/', views.alumni_dash, name='alumni_dash'),
    path('roles/update_user_status/', views.update_user_status, name='update_user_status'),
    path('enq/', views.enq, name='enq'),
    path('load/<str:page>/', views.load_admin_page, name="load_admin_page"),
    path('jobpost/', views.jobpost, name='jobpost'),
    path('save-profile/', views.save_profile, name='save_profile'),
    path('profile-photo/<str:profile_id>/', views.serve_profile_photo, name='profile_photo'),
    path("update_job_status/", views.update_job_status, name="update_job_status"),
    path("send-mentorship/<str:alumni_id>/", views.send_mentorship_request, name="send_mentorship"),
    path("roles/alumni_dash/", views.alumni_dash, name="alumni_dash"),
    path("roles/alumni/<str:page>/", views.load_alumni_page),
    path(
        "profile-photo/<str:profile_id>/",
        views.serve_profile_photo,
        name="serve_profile_photo"
        ),
    path(
    "update-mentorship-status/",
    views.update_mentorship_status,
    name="update_mentorship_status"
),
path(
    "student/chat/<str:mentorship_id>/",
    views.student_chat,
    name="student_chat"
),
path("student/chat/<str:mentorship_id>/", views.private_chat, name="private_chat"),
path("student/chat/<str:mentorship_id>/send/", views.send_private_message, name="send_private_message"),
path('verify-email/<str:email>:<str:token>/', views.verify_email, name='verify_email')
]
