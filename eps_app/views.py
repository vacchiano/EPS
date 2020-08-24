from django.shortcuts import render, HttpResponse, redirect
from log_reg_app.models import User, Work_Day, Points, Daily_Report
from datetime import datetime, timedelta
# from eps_app.functions import time


# Create your views here.

def home(request):
    if 'clocked_in' not in request.session:
        request.session['clocked_in'] = False

    work_days = Work_Day.objects.all()
    clocked_in = request.session['clocked_in']
    user = User.objects.get(id=request.session['user_id'])
    all_users = User.objects.all()
    context = {
        'work_days' : work_days,
        'clocked_in' : clocked_in,
        'user': user,
        'all_users': all_users,
        # 'times' : time

    }
    return render(request, 'eps_app/home.html', context)

def points(request):
    return render(request, 'eps_app/points.html')

def daily_report(request):
    return render(request, 'eps_app/daily_report.html')

def settings(request):
    return render(request, 'eps_app/settings.html')

def forgot(request):
    return render(request, 'eps_app/forgot_form.html')

def clockin(request):

    user = User.objects.get(id=request.session['user_id'])
    request.session['clocked_in'] = True
    work_day = Work_Day.objects.create(
        date=datetime.date.today(),
        total_time= 0,
        desc='hello everybody',
        user=user,
    )
    request.session['work_day_id'] = work_day.id
    return redirect('/eps/home')

def clockout(request):
    request.session['clocked_in'] = False
    work_day = Work_Day.objects.get(id=request.session['work_day_id'])
    work_day.clockout = datetime.date.today()
    work_day.save()
    del request.session['work_day_id']
    return redirect('/eps/home')
