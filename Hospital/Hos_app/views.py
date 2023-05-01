from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Departments, Doctors,Booking
from .forms import BookingForm
from django.contrib.auth import authenticate , login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .forms import  UserRegistrationForm , UserLoginForm, UserUpdateForm, SetPasswordForm, PasswordResetForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.db.models.query_utils import Q

# Create your views here.

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account")
        return redirect ('login')
    else:
        messages.error(request, "Activation link is invalid!")
    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message =  render_to_string("accounts/template_activate_account.html", {
         'user': user.username,
         'domain': get_current_site(request).domain,
         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
         'token': account_activation_token.make_token(user),
         "protocol": 'https' if request.is_secure() else 'http'
         })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
                          received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@user_not_authenticated
def registerpage(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))    
            return redirect('register')

        else:
            for error in list(form.errors.values()):
                print(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name = "accounts/register.html",
        context={"form": form}
    )

@user_not_authenticated
def loginpage(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username = request.POST['username'],
                password = request.POST['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"You have been logged in....")
                return redirect('index')
        else:
            for key, error in list(form.errors.items()):
                 if key == 'captcha' and error[0] == 'This field is required.':
                     messages.error(request, 'You must pass the reCAPTCHA test')
                     continue
                 
                 messages.error(request, error)

    form = UserLoginForm()

    return render(
        request=request,
        template_name="accounts/login.html",
        context={"form":form}
    )

@login_required
def profile(request, username):
    if request.method == "POST":
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form =form.save()
            messages.success(request, f'Your profile has been updated! Now you can login your account.')
            return redirect("profile", user_form.username)
        
        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    booked = {'profile':Booking.objects.filter(p_name=username)}
    
    if user :
        form = UserUpdateForm(instance=user)
        return render(
            request=request,
            template_name="profile.html",
            context={"form":form},
        )

    return redirect(request, "login",booked)

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'accounts/password_reset_confirm.html', {'form' : form})

@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            assosiated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if assosiated_user:
                subject = "Password Reset request"
                message =  render_to_string("accounts/template_reset_password.html", {
                    'user': assosiated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(assosiated_user.pk)),
                    'token': account_activation_token.make_token(assosiated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                    })
                email = EmailMessage(subject, message, to=[assosiated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        Password reset sent.  

                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, SERVER PROBLEM !")
                
            return redirect('home')
        
        for key, error in list(form.errors.items()):
                 if key == 'captcha' and error[0] == 'This field is required.':
                     messages.error(request, 'You must pass the reCAPTCHA test')
                     continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name='accounts/password_reset.html',
        context={'form': form}
    )


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():       
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and log in now !")
                return redirect("home")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form':form})
    else:
        messages.error(request, "Link is expired!")
    messages.error(request, 'Somthing went wrong, redirecting back to homepage')
    return redirect("home")


@login_required
def logoutpage(request):
    logout(request)
    messages.success(request, ("You Where Logged Out!"))
    return redirect('home')

def home(request):
    return render(request,'accounts/home.html')

@login_required
def index(request):
    dict_dept = {
        'dept':Departments.objects.all()
    }
    return render(request,'index.html',dict_dept)

@login_required
def about(request):
    return render(request,'about.html')

@login_required
def booking(request,id=0):
    if request.method == "GET":
        if id == 0:            
            form = BookingForm()
        else:
            booking = Booking.objects.get(pk=id)
            form = BookingForm(instance=booking)
        return render(request,"booking.html", {'form':form})
    else:
        if id == 0:
            form = BookingForm(request.POST)
        else:
            booking = Booking.objects.get(pk=id)
            form = BookingForm(request.POST,instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, ("We have received your appointment request, our representative will call you shortly.!"))
        return redirect("booking")

@login_required   
def booking_delete(request, id):
    booking = Booking.objects.get(pk=id)
    booking.delete()
    return redirect("profile")

def doctors(request):
    dict_docs = {
        'doctors':Doctors.objects.all()
    }
    return render(request,'doctors.html', dict_docs)

def department(request):
    dict_dept = {
        'dept':Departments.objects.all()
    }
    return render(request,'department.html', dict_dept)

