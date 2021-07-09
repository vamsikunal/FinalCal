from django.shortcuts import render
from .forms import UserForm, EventForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar
from django.views import generic
import calendar
from django.views.generic import View
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from .utils import Calendar
from .models import Event


# Class based view for base
class base(TemplateView):
    template_name = 'base.html'

# Function based view for registration form
def register(request):
    user_form = UserForm(request.POST or None)

    if request.method == 'POST':
         if user_form.is_valid(): # Check the form validity

             user = user_form.save() # Saving the data to database
             user.set_password(user.password)  # set_password method used to save the password in hashed form
             user.save()  # Saved the hashed password and user
             return HttpResponseRedirect(reverse('app:login'))

         else:
             print(user_form.errors)
    return render(request, 'register.html', {'user_form': user_form})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password) # checks for authentication of the user automatically

        if user:
                login(request,user) # django inbuilt function for login
                return HttpResponseRedirect(reverse('app:calendar'))
        else:
            return render(request, "login.html", {'message': "Username and Password are incorrect"})
    else:
        return render(request,'login.html',{})

@login_required # decorators used if person is logged in
def user_logout(request):
    logout(request) # django inbuilt function for logout
    return HttpResponseRedirect(reverse('app:base'))

class about (TemplateView):
    template_name = 'about.html'

def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('app:calendar'))
    return render(request, 'event.html', {'form': form})

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1) # Gives first day of month
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def CalanderView(request):
    d = get_date(request.GET.get('month', None))
    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(withyear=True)
    event_list = Event.objects.order_by('start_time')
    today = date.today()
    month = d.month
    user=request.user
    return render(request, 'home.html', {'calendar': mark_safe(html_cal), # make_safe in django is used to make html calendar
                                          'prev_month': prev_month(d),
                                          'next_month': next_month(d),
                                          'month':month,
                                          'today':today,
                                          'event':event_list,
                                           'user':user})

def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'event_detail.html', context)

class event_details(TemplateView, ListView):
