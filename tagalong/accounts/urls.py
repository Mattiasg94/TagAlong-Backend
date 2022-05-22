from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from accounts import api


urlpatterns = [
    path(r'api/user/<str:pk>/', api.UserById.as_view()),
    path(r'api/allUsers/', api.GetAllUser.as_view()),
    path(r'api/friend-request/', api.HandleFriendRequest.as_view()),
    path(r'api/friend-request/<str:pk>/', api.FriendRequestById.as_view()),
    path(r'api/friend-request/<str:pk>/<str:to_or_from>/',
         api.FriendRequestById.as_view()),
    path(r'api/eventUsers/<str:pks>/', api.GetEventUsers.as_view()),
    path(r'api/email/<str:pks>/<str:action>/<str:target>/',
         api.SendEmailToUsers.as_view()),



    path(r'my-events/', accounts_views.my_events, name='my_events'),
    path(r'profile/', accounts_views.profile, name='profile'),
    path(r'signup/', accounts_views.signup, name='signup'),
    path(r'login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(r'reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             email_template_name='password_reset_email.html',
             subject_template_name='password_reset_subject.txt'
         ),
         name='password_reset'),
    path(r'settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change'),
    path(r'settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),
    path(r'reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'),    name='password_reset_done'),
    path(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'),        name='password_reset_confirm'),
    path(r'reset/complete/',        auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'),       name='password_reset_complete'),
    path('verify-email/<uidb64>/<token>/',
         accounts_views.verify_email, name='verify_email'),
]
