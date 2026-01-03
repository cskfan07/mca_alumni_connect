from mongoengine import (Document, StringField, IntField, EmailField,
                         BooleanField,DateTimeField,FileField,ReferenceField)
from datetime import datetime
from django.utils import timezone
class User(Document):
    username = StringField(required=True)
    roll_no = IntField(required=True)
    reg_no =StringField(required=True)
    email = EmailField(required=True, unique=True)
    email_token = StringField()
    password = StringField(required=True)
    passout_Year = IntField(required=True)
    role=StringField(required=True)
    is_Verified =  IntField(default=0) # 0 = not approved, 1 = approved, -1 = rejected
    is_Active=BooleanField(default=False)
    created_on=DateTimeField(default=timezone.now)


class Enquiry(Document):
    name = StringField(required=True)
    email = EmailField(required=True)  # removed unique=True
    message = StringField(required=True)
    time = DateTimeField(default=datetime.utcnow)


class JobPost(Document):
    title = StringField(required=True)
    type = StringField(required=True)
    company = StringField(required=True)
    description = StringField(required=True)
    link = StringField(required=True)
    user_id = StringField(required=True)
    expiry = DateTimeField(required=True)
    post_status= IntField(default=0)   # 1 for approve , -1 for reject
    created_at = DateTimeField(default=timezone.now)
    meta = {
        'collection': 'job_posts'   # NEW COLLECTION NAME
    }

class Profile(Document):
    user = ReferenceField(User, required=True, unique=True)
    curnt_wrk_role = StringField()
    dob = StringField()
    age = StringField()
    skill = StringField()
    cwc = StringField()
    loc = StringField()
    ph = StringField()
    wexp = StringField()
    llink = StringField()
    bio = StringField()
    photo = FileField()

class MentorshipRequest(Document):
    student = ReferenceField(User, required=True)
    alumni = ReferenceField(User, required=True)
    message = StringField(default="Please guide me.")
    status = StringField(default="pending")  # pending / accepted / rejected
    created_at = DateTimeField(default=datetime.now)

class PrivateChat(Document):
    mentorship_id = ReferenceField(MentorshipRequest)
    student_id = ReferenceField(User)
    alumni_id = ReferenceField(User)
    sender_id = ReferenceField(User)
    message = StringField()
    timestamp = DateTimeField(default=datetime.utcnow)

class GroupChat(Document):
    sender_id = ReferenceField(User)
    message = StringField()
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'groupchat'}

class Notification(Document):
    user = ReferenceField(User, required=True)
    message = StringField(required=True)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'notifications'
    }
