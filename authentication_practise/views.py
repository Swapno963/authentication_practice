from . import forms 
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Register Successfully.')
            return redirect('profile')
    else:
        register_form = forms.RegistrationForm()
    return render(request, 'register.html',{'form':register_form, 'type':'Register'})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username=user_name, password = user_pass)
            if user is not None:
                login(request, user)
                messages.success(request,'Login Successfylly.')
                return redirect('profile')
            else:
                messages.warning(request, 'Login Information Is Incorrenct')
                return redirect('profile')
            
    else:
        form = AuthenticationForm()
    return render(request, 'register.html', {'form':form, 'type':'Login'})


@login_required
def user_profile(request):
    return render(request, 'user_profile.html',{'user':request.user})
    

def user_logout(request):
    logout(request)
    return redirect('user_longin')


def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully.')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html',{'form':form})

def pass_chang_without(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.usesr)
            return redirect('user_longin')
        
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'pass_change_without.html',{'form':form})
