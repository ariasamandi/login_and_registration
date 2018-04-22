# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.
def index(request):
    return render(request, 'my_app/index.html')
def process_register(request):
    # if request.method == "POST":
    #     return redirectp
    error = False
    if len(request.POST['first_name']) < 2:
        messages.error(request, "first name should be longer than 2 characters")
        error = True
    if not request.POST['first_name'].isalpha():
        messages.error(request, "first name should be only letters")
        error = True
    if not request.POST['last_name'].isalpha():
        messages.error(request, "last name should be only letters")
        error = True
    if len(request.POST['last_name']) < 2:
        messages.error(request, "last name should be longer than 2 characters")
        error = True
    if len(request.POST['password']) < 8:
        messages.error(request, "password should be longer than 8 characters")
        error = True
    if request.POST['password'] != request.POST['confirm_password']:
        messages.error(request, "passwords dont match")
        error = True
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, "Email is invalid")
        error = True
    if len(User.objects.filter(email=request.POST['email'])) > 0:
        messages.error(request, "Email taken")
        error = True
    if error:
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        the_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], 
        email=request.POST['email'], password=hash1)
        print the_user
        request.session['user_id'] = the_user.id
        return redirect('/success')
def process_login(request):
    #  if request.method == "POST":
    #      return redirect('/success')
    the_user_list = User.objects.filter(email = request.POST['email'])
    if len(the_user_list) > 0:
        the_user = the_user_list[0]
    else:
        messages.error(request, "Email or password invalid")
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), the_user.password.encode()):
        request.session['user_id'] = the_user.id
    else:
        messages.error(request, "Email or password invalid")
    return redirect('/success')
def success(request):
    if not 'user_id' in request.session:
        messages.error(request, "Must be logged in")
        return redirect('/')
    context = {
        "User": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'my_app/success.html', context)
def logout(request):
    request.session.clear()
    return redirect('/')