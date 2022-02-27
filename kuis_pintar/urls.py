from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetConfirmView

from graphene_django.views import GraphQLView
from app.schema import schema

from app import views
from app import forms

urlpatterns = [
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('kuis/', views.kuis, name='kuis'),
    path('profile/', views.profile, name='profile'),
    path('get_data/', views.get_data, name='get_data'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/get', views.get_feedback, name='get_feedback'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/',views.logout_view, name='logout'),
    path('login/',
         LoginView.as_view
         (
             template_name='auth/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             redirect_authenticated_user=True,
             extra_context=
             {
                 'title': 'Login',
             }
         ),
         name='login'),
]
