from django.shortcuts import render , redirect
from .forms import UserRegistrationForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
from .opt_generator import generate_otp


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1'] 


            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['password1'] = password

            subject = 'Your OTP for verification'

            context = {
                'otp': otp
            }
            message = render_to_string('otp_email_template.html', context)

            send_mail(
                subject,
                message,
                'manishaharijan94@gmail.com',
                [email],
                fail_silently=False,
                html_message=message, 
            )
            messages.success(request, f'otp sent to {email}')
            return redirect('verify_otp')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/register.html', context)


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == str(request.session.get('otp')):
            email = request.session.get('email')
            password = request.session.get('password1')

            user = User.objects.create_user(username=email, email=email)
            user.set_password(password) 
            user.save()
            subject = 'Thank you for registering with us'

            context = {
                'email': email
            }
            message = render_to_string('register_successful.html', context)

            send_mail(
                subject,
                message,
                'manishaharijan94@gmail.com',
                [email],
                fail_silently=False,
                html_message=message, 
            )
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            return render(request, 'dashboard/verify_otp.html', {'error': 'Invalid OTP.'})
    return render(request, 'dashboard/verify_otp.html')
        

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.username}! You are now logged in.')
                return redirect('home')  
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'dashboard/login.html', {'form': form})

@login_required(login_url='login')
def lougout_view(request):
    logout(request)
    return redirect('login')
