# Cords Social

1. [FEATURES](#features)
2. [HOW TO INSTALL](#installation)
    - [MANUALLY INSTALLING DEPENDENCIES](#manually-installing-dependencies)
3. [USING OTHER DATABASES](#using-a-different-database)
4. [SCREENSHOTS](#screenshots)
   - [Login](#login-page)
   - [Register](#registration-page)
   - [Home Page](#home-page)
   - [Create Post](#create-post)
   - [Search](#search)
   - [Chat](#chat)
   - [Settings](#settings)
   - [Admin Dashboard](#django-admin-dashboard)

## Features 
- Login
- Registration
- Logout
- Profile Customization (username, email, password, display name, bio, profile picture, banner)
- Create/Delete posts
- Like/Unlike
- Comment/Delete comment
- Follow/Unfollow
- Send/Delete a message
- Search users
- Notifications
- Admin dashboard (built-in)

## Installation

NOTE: These steps are for Ubuntu/Debian based systems, however, Windows and MacOS will have nearly identical steps.

1. Install Python 3 on your system.
2. Install pip. We will use pip to install the required dependencies.
   
   ```
   sudo apt install python3-pip
   ```
3. Install required dependencies from requirements.txt.
   
   ```
   pip install -r requirements.txt
   ```
4. Make migrations to database

   ```
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

5. Create an admin user to access the Django admin dashboard `/admin`.

   ```
   python3 manage.py createsuperuser
   ```
7. Run the development server. If you get an error saying a module was not found, see [manually installing dependencies](#manually-installing-dependencies)

   ```
   python3 manage.py runserver
   ```

### Manually Installing Dependencies
If this does not work then try installing the exact version of the packages listed in requirements.txt
   ```
   pip install django daphne channels
   ```

## Using a Different Database

To use a database other than SQLite3, please see [docs.djangoproject.com/en/5.0/ref/databases](https://docs.djangoproject.com/en/5.0/ref/databases/)

## Screenshots

### Login Page 

![Login Page](./screenshots/login.png)

### Registration Page

![Registration Page](./screenshots/register.png)

### Home Page

![Home Page](./screenshots/home.png)

### Create Post

![Create Post](./screenshots/post.png)

### Search 

![Search](./screenshots/search.png)

### Chat

![Chat](./screenshots/chat.png)

### Settings 

![Profile Personalization](./screenshots/profile_personalize.png)

![Account Options](./screenshots/account_options.png)

## Django Admin Dashboard

![Admin Dashboard](./screenshots/admin.png)

