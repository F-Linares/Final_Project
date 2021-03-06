from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from datetime import datetime

# Create your views here.

def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user':User.objects.get(id=request.session['user_id']),
        'trips': Trip.objects.all(),
    }
    return render(request, 'home.html', context)

def showTrip(request, tripId):
    if 'user_id' not in request.session:
        return redirect('/')
    context={
        'trips': Trip.objects.get(id=tripId),
        'user': User.objects.get(id = request.session['user_id']),
    }
    return render(request, 'trips.html', context)

def delete(request, tripId):
    if 'user_id' not in request.session:
        return redirect('/')
    Trip.objects.get(id=tripId).delete()
    return redirect('/dashboard')

def edit(request, tripId):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'trips': Trip.objects.get(id=tripId),
        'user': User.objects.get(id = request.session['user_id']),
    }
    return render(request, 'edit.html', context)

def update(request, tripId):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Trip.objects.edit_validators(request.POST)
    if len(errors):
        for error in errors.values():
            messages.error(request, error)
        return redirect(f'/dashboard/edit/{tripId}')
    else:
        updated = Trip.objects.get(id=tripId)
        updated.destination = request.POST['updated_destination']
        updated.start_date = request.POST['updated_start_date']
        updated.end_date = request.POST['updated_end_date']
        updated.plan = request.POST['updated_plan']
        updated.save()
        return redirect(f'/dashboard')

def add(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'add.html')

def addTrip(request):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors):
        for error in errors.values():
            messages.error(request, error)
        return redirect('/dashboard/add')
    else:
        Trip.objects.create(
            destination = request.POST['destination'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            plan = request.POST['plan'],
            trip_member = User.objects.get(id = request.session['user_id']),
        )
        return redirect('/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')