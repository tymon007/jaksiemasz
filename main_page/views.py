import hashlib
import json
import random
import re
import string
import uuid
from django.utils import timezone
import pytz

import matplotlib
from django.shortcuts import render, redirect

matplotlib.use('Agg')
from matplotlib import dates as mpl_dates
from matplotlib import pyplot as plt

from .models import User, Post

from datetime import datetime
import time
import os

from rich import print


def md5(s, raw_output=False):
    res = hashlib.md5(s.encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def f_salt():
    return (md5(str(uuid.uuid4)))[0:-8]


def main_page(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        return render(request, 'main_page/index.html', context={
            'is_logged_key': True
        })
    else:
        return render(request, 'main_page/not_login_index.html', context={
            'is_logged_key': False
        })


def log_in(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        return redirect('main_page')
    else:
        errors = request.session.get('errors', False)
        request.session['errors'] = False
        return render(request, 'registration/login.html', context={
            'is_logged_key': False,
            'errors': errors
        })


def auth_login(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        return redirect('main_page')
    else:
        errors = []

        req_username = request.POST.get('username')
        req_password = request.POST.get('password')

        user = User.objects.filter(username=req_username)

        if len(user) > 0:
            if md5(md5(req_password) + user[0].salt) == user[0].password:
                request.session['is_logged'] = True
                request.session['id_user'] = user[0].id
                return redirect('main_page')

        errors.append('Some errors detected: Form is not valid')
        request.session['errors'] = errors
        return redirect('log_in')


def sign_in(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        return redirect('main_page')
    else:
        errors = request.session.get('errors', False)
        request.session['errors'] = False
        return render(request, 'registration/signup.html', context={
            'is_logged_key': False,
            'errors': errors
        })


def auth_sign_in(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        return redirect('main_page')
    else:
        errors = []

        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # username validation
            users = User.objects.filter(username=username)
            if len(users) != 0:
                errors.append('Some errors detected: account with this username already exist')
            else:
                for char in username:
                    if char.isalpha() or char.isdigit():
                        continue
                    else:
                        errors.append('Some errors detected: username contains not allowed character(s)')
                        break

            # email validation
            regex = "^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*(\\.\\w{2,3})+$"
            if not re.search(regex, email):
                errors.append('Some errors detected: email is not valid')

            # password validation
            if password1 == "" and password2 == "":
                errors.append('Some errors detected: passwords can\'t be empty')
            else:
                if password1 != password2:
                    errors.append('Some errors detected: passwords do not match')
                else:
                    if len(password1) < 5:
                        errors.append('Some errors detected: password length must be at least 5 characters')
                    else:
                        pass

            if len(errors) == 0:
                salt = f_salt()
                password = md5(md5(password1) + salt)

                User.objects.create(
                    username=username,
                    email=email,
                    password=password,
                    salt=salt
                )

                user_id = User.objects.filter(username=username)[0].id

                request.session['is_logged'] = True
                request.session['id_user'] = user_id
                return redirect('main_page')

        else:
            errors.append('Some errors detected: Method is not POST')

        request.session['errors'] = errors
        return redirect('sign_in')


def logout(request):
    # checking if user logged in
    request.session['is_logged'] = False
    request.session['id_user'] = False
    return redirect('main_page')


def me(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        user = User.objects.filter(id=request.session.get('id_user'))[0]
        return render(request, 'aboutMe/me.html', context={
            'is_logged_key': True,
            'user': user
        })
    else:
        return redirect('log_out')


def porady(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        return render(request, 'environment/porady.html', context={
            'is_logged_key': True
        })
    else:
        return redirect('log_out')


def credits(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        return render(request, 'credits.html', context={
            'is_logged_key': True
        })
    else:
        return redirect('log_out')


def http_not_found(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        return render(request, '404.html', context={
            'is_logged_key': True
        })
    else:
        return redirect('log_out')


def lekarze(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        return render(request, 'lekarze.html', context={
            'is_logged_key': True
        })
    else:
        return redirect('log_out')


def Calendar(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)
    if is_logged:
        return render(request, 'environment/Calendar.html', context={
            'is_logged_key': True
        })
    else:
        return redirect('log_out')


def sendpostcal(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)

    if is_logged:
        if request.method == 'POST':
            user_id_s = request.session.get('id_user', False)

            mood_data_list = json.loads(request.POST.get("mood-data"))
            print(mood_data_list)

            if len(mood_data_list) != 0:
                for elem in mood_data_list:
                    # datew = date.fromtimestamp(int(elem["date"]))
                    timestamp = elem["date"]
                    dt_object = datetime.fromtimestamp(timestamp / 1000)

                    Post.objects.create(
                        user_id=User.objects.get(id=user_id_s),
                        content=elem["text"],
                        well_being=elem["mood"],  # "here should be well-being from form"
                        food=5,  # "here should be I dunno even what and from where" 2020-09-27T22:00:00.000Z
                        icon="icon.txt",
                        date=dt_object
                    )

                posts = Post.objects.filter(user_id=user_id_s).order_by('date')

                plt.style.use('fivethirtyeight')

                dates = []
                well_being = []

                for post in posts:
                    dates.append(post.date)
                    well_being.append(post.well_being)

                plt.plot_date(dates, well_being, linestyle='solid', linewidth="2", marker="o", color='#4c96d7')

                plt.gcf().autofmt_xdate()

                date_format = mpl_dates.DateFormatter('%b, %d %Y')
                plt.gca().xaxis.set_major_formatter(date_format)
                plt.gca().set_facecolor('#f8f9fa')

                plt.title("Wykres samopoczucia")
                plt.xlabel("Miesiąc")
                plt.ylabel("Samopoczucie")

                plt.tight_layout()

                dir = os.path.join("/", "opt", "lampp", "htdocs", "main_page", "static", "images",
                           "auto-generated-charts", "user-" + str(user_id_s))
                if not os.path.exists(_dir):
                    os.mkdir(_dir)

                plt.savefig(
                    '/opt/lampp/htdocs/main_page/static/images/auto-generated-charts/user-'
                    + str(user_id_s) + '/last_well_being.png',
                    format="png")
            else:
                pass
        else:
            pass

        return redirect('wykresy')
    else:
        return redirect('log_out')


def wykresy(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)

    if is_logged:
        user_id_s = request.session.get("id_user", False)
        posts = Post.objects.filter(user_id=user_id_s).order_by('date')

        return render(request, 'post-related-pages/wykresy.html', context={
            'is_logged_key': True,
            'posts': posts,
            'static_chart_name': 'images/auto-generated-charts/user-' + str(user_id_s) + '/last_well_being.png'
        })
    else:
        return redirect('log_out')
