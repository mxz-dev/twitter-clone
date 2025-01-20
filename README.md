# My Django Twitter Clone App 

Welcome to **Django Twitter Clone App**! This is a [Django](https://www.djangoproject.com/) application designed to [challenge my skills].

## Features
- Authentication The Users
- Add, modify, remove, view tweets 
- Like and dislike tweets
- Follow and unfollow users
- Change User settings
- Change User Profile (image, BIO, email, social media) 

## Prerequisites
Before getting started, make sure you have the following installed on your system:
- [Docker](https://www.docker.com/) (with Docker Compose)
- Git

## Quick Start

Follow these steps to run the project on your local machine:

### 1. Clone the Repository From Github and Run's with docker compose (Recommended)
```bash
git clone https://github.com/mxz-dev/twitter-clone.git
cd twitter-clone
docker-compose up --build
```
### 2. Run & install Manualy (Optional)
```bash
cd twitter-clone
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
