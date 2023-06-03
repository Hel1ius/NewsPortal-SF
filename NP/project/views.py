from django.shortcuts import redirect


def home(requests):
    return redirect('/news')