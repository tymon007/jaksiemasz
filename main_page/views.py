import hashlib
import random
import re
import string
import uuid

from django.shortcuts import render, redirect
import matplotlib
matplotlib.use('Agg')
from matplotlib import dates as mpl_dates
from matplotlib import pyplot as plt
from datetime import datetime

from .models import User, Post


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
        return redirect('log_out')


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
    return redirect('log_in')


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
        return render(request, 'porady.html', context={
            'is_logged_key': True
        })
    else:
        return redirect('log_out')

def credits(request):
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


def wykresy(request):
    # checking if user logged in
    is_logged = request.session.get('is_logged', False)

    if is_logged:
        user_id_s = request.session.get('id_user', False)

        posts = Post.objects.filter(user_id=user_id_s).order_by('date')

        plt.style.use('fivethirtyeight')

        dates = []
        well_being = []

        for post in posts:
            dates.append(post.date)
            well_being.append(post.well_being)

        plt.plot_date(dates, well_being, linestyle='solid', linewidth="1", marker=".", color="red")

        plt.gcf().autofmt_xdate()

        date_format = mpl_dates.DateFormatter('%b, %d %Y')
        plt.gca().xaxis.set_major_formatter(date_format)

        plt.title("Chart")
        plt.xlabel("Month")
        plt.ylabel("Well-being")

        plt.tight_layout()

        # static_path_to_chart = ('images/auto-generated-charts/user-' + str(user_id_s) + '/well_being@'
        #                         + datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + '@' + str(uuid.uuid1()) + '.png')
        #
        # plt.savefig('d:/projects/Django/django_projects/skrrt/main_page/static/' + static_path_to_chart,
        #             format="png")

        static_path_to_chart = ('images/auto-generated-charts/user-2/'
                                'well_being@10-20-2020_11-05-17@5fba488e-12b3-11eb-8711-9828a61b3b5c.png')

        return render(request, 'post-related-pages/wykresy.html', context={
            'is_logged_key': True,
            'posts': posts,
            'static_chart_name': static_path_to_chart
        })
    else:
        return redirect('log_out')
