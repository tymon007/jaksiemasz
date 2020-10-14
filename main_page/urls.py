from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$',                    views.main_page,          name='main_page'),
    re_path(r'^log_in/$',             views.log_in,             name="log_in"),
    re_path(r'^auth_login/$',         views.auth_login,         name="auth_login"),
    re_path(r'^sign_in/$',            views.sign_in,            name='sign_in'),
    re_path(r'^auth_sign_in/$',       views.auth_sign_in,       name="auth_sign_in"),
    re_path(r'^logout/$',             views.logout,             name="log_out"),
    re_path(r'^me/$',                 views.me,                 name="me"),
    re_path(r'^credits/$',            views.credits,            name="credits"),
    re_path(r'^.*$',                  views.http_not_found,     name="not_found"),
]
