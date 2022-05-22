from multiprocessing import context
from django.utils.encoding import force_bytes
from accounts.models import User
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from accounts.forms import SignUpForm
from django.core.mail import send_mail, BadHeaderError
import logging
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from tagalong.settings import EMAIL_HOST_USER, config
from website.models import Event
from accounts.forms import UserForm
logger = logging.getLogger("mylogger")



def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model()._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        message = f"""
        <h2 class="mt-3">Du är en av oss nu! <i class="far fa-grin-hearts" style="color: green;"></i> <i class="fas fa-leaf" style="color: green;"></i></h2>
        <h5>Tack för verifieringen, du kan nu logga in.</h5>
        """
    else:
        message = """
        <h2 class="mt-3">Oj något gick fel</h2>
        <h5>Invalid aktiveringslink. Du kanske tryckte på en gammal link</h5>"""
    return render(request, 'message.html', {'message': message})


def signup(request):
    #TODO no regex on username
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get('email')
            if User.objects.filter(email=to_email).exists():
                form.add_error('email', 'Email already exists')
                return render(request, 'signup.html', {'form': form})
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            # Profile.objects.create(user=user)
            current_site = get_current_site(request)
            subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            # try:
            #     send_mail(subject, message, EMAIL_HOST_USER, [to_email])
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found.')
            message = f"""
                    <h2 class="mt-3">Du är snart klar! <i class="fas fa-envelope" style="color: green;"></i></h2>
                    <p>Ett verifieringsmejl från tagalong@gmail.com har skickats till {to_email}.</p>
                    <p style="color:red;">Kolla din skräppost</p>
                    """
            return render(request, 'message.html', {'message': message})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile(request):
    context={}
    user_form=UserForm(instance=request.user)
    context['user_form']=user_form
    if request.method=="POST":
        # User.objects.get(user=request.user)
        form=UserForm(request.POST, request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.INFO,f'Profile has been updated.')
    return render(request, 'accounts/profile.html',context)

@login_required
def my_events(request):
    context={}
    events=Event.objects.filter(user=request.user).order_by('date')
    context['events']=events
    if request.method=="POST":
        action=request.POST['action']
        if action=='delete':
            event=Event.objects.get(pk=request.POST['event_id'])
            messages.add_message(request,messages.INFO,f'Event {event.title} has been deleted.')
            event.delete()
    return render(request, 'accounts/my-events.html',context)
