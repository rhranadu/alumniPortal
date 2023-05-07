from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from .utils import generate_token, TokenGenerator

# Create your views here.
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password1']
        confirmPassword = request.POST['password2']
        if password != confirmPassword:
            messages.warning(request, "Passwords don't match!")
            return render(request, "authentication/signup.html")            
        try:
            if User.objects.get(username=email):
                messages.warning(request, "User already exist!")
                return render(request, "authentication/signup.html")            
        except Exception as ide:
            pass            
        user = User.objects.create_user(name, email, password)
        user.is_active = False
        user.save()    
        email_subject = "New Alumni registered"
        message = render_to_string('authentication/activate.html',
                                   {
                                       'user':user,
                                       'domain':'127.0.0.1:8000',
                                       'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token':generate_token.make_token(user)
                                   })
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, ['anandvishnug1994@gmail.com'] )
        email_message.send()
        messages.success(request, "Your account is being verified, once activated you will get an email")
        return render(request, "authentication/signin.html")
    return render(request, "authentication/signup.html")
class ActivateAccountView( View ):
    def get(self, request, uidb64, token):
        try:
            uid= force_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(pk=uid)
        except Exception as ide:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True 
            user.save()
            email_subject = "Account activated"
            message = render_to_string('authentication/account_verified.html',
                                    {
                                        'user':user,
                                        'domain':'127.0.0.1:8000',
                                    })
            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [user.email] )
            email_message.send()
            
            messages.info(request, "Account activated successfully!")
            return redirect('/auth/signin/')
        return render(request,'authentication/activatefail.html')

def handleSignIn(request):
    if request.method == 'POST':
        name = request.POST['name']
        # email = request.POST['email']
        password = request.POST['password1']
        # print(f"{email} and {password}")
        user = authenticate(username= name, password=password)
        print(f"{user}")
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("/auth/signin/")
    return render(request, "authentication/signin.html")
def handleSignOut(request):
    logout(request)
    messages.success(request, "Logout successfull!")
    return redirect("/")