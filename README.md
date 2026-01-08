 
 

 
# 🎓 MCA Alumni Connect Platform

MCA Alumni Connect is a role-based web application developed using Django, and database used mongoDB atlas.
The platform is designed to connect MCA students, alumni, and administrators
to enable communication, mentorship, job sharing, and alumni networking.

---

## 📌 Project Overview

The MCA Alumni Connect Platform provides separate dashboards and functionalities
for **Students**, **Alumni**, and **Admin** users.  
Each user role has its own access level, menus, and features.

The system helps students interact with alumni for guidance and career
opportunities, while administrators manage and monitor the platform.

---

## 🏗️ Project Structure

 

mca_alumni_connect/
│── manage.py
│── requirements.txt
│── build.sh
│
├── mca_alumni_connect/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── users/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── mongo.py
│   ├── migrations/
│   ├── static/
│   └── templates/
│
│       ├── roles/
│       │   ├── admin_menu/
│       │   ├── alumni_menu/
│       │   └── student_menu/
│       │
│       ├── login.html
│       ├── register.html
│       ├── landing.html
│       ├── dashboard.html
│       ├── admin_panel.html
│       ├── alumni_dash.html
│       └── student_dash.html
 

---

## 👥 User Roles & Features

### 👨‍🎓 Student Module
- Student registration and login
- Student dashboard
- Alumni directory access
- Chat with alumni
- View job opportunities
- File management
- Profile management

Templates:
 

roles/student_menu/

* dash_std_menu.html
* chat_std_menu.html
* job_std_menu.html
* alumni_dir_menu.html
* myfile_std_menu.html
* profile_std_menu.html

 

---

### 🧑‍💼 Alumni Module
- Alumni registration and login
- Alumni dashboard
- Chat with students
- Job posting and viewing
- Mentorship support
- File uploads
- Profile management

Templates:
 

roles/alumni_menu/

* a_dash_menu.html
* chat_a_menu.html
* job_a_menu.html
* mentor_a_menu.html
* myfile_a_menu.html
* profile_a_menu.html

 

---

### 🛠️ Admin Module
- Admin authentication
- Admin dashboard
- Manage users (students & alumni)
- Post management
- Enquiry handling
- Profile management
- System monitoring

Templates:
 

roles/admin_menu/

* dashboard_menu.html
* chat_menu.html
* post_menu.html
* profile_menu.html
* f_enq.html

 

---

## 🔐 Authentication Flow

1. User lands on the landing page
2. Registers or logs in
3. Role is identified (Student / Alumni / Admin)
4. User is redirected to the respective dashboard
5. Access is granted based on role permissions

---

## 🧰 Technology Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Optional DB:** MongoDB (for chat or extended features)
- **Authentication:** Django Authentication System
- **Version Control:** Git & GitHub

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
 bash
git clone https://github.com/your-username/mca-alumni-connect.git
 

### 2️⃣ Navigate to Project Directory

 bash
cd mca-alumni-connect
 

### 3️⃣ Create Virtual Environment

 bash
python -m venv venv


### 4️⃣ Activate Virtual Environment (Windows)

 bash
venv\Scripts\activate
 

### 5️⃣ Install Dependencies

 bash
pip install -r requirements.txt
 
 
### 8️⃣ Run the Server

 bash
python manage.py runserver
 

---

## 🚀 Usage

Open browser and visit:

 
http://127.0.0.1:8000/
 
 

## 🔮 Future Enhancements

* Real-time chat system
* Job application module
* Email notifications
* Mobile responsive UI
* Advanced alumni-student mentorship system

---

## 🤝 Contributing

Contributions are welcome.
Fork the repository and submit a pull request for improvements.

---

## 👤 Author

**ANKIT KUMAR GUPTA**
MCA Student
GitHub: [https://github.com/cskfan07](https://github.com/cskfan07)
 
I also deploy on render link: (https://mca-alumni-connect.onrender.com)
