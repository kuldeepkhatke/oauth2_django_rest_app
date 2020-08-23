from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework import status, viewsets
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .forms import LoginForm, UserCreationForm, TaskCreationForm
from .models import Task
from .serializers import TaskSerializer, LoginSerializer, RegisterSerializer
from oauth2_provider.models import Application
from django.db.models import Q
import requests
from django.conf import settings 

class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

# API VIEWS
class TaskView(viewsets.ModelViewSet):
    """
    Task viewset.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tasks = Task.objects.filter(Q(created_by=self.request.user)|Q(assigned_to__id=self.request.user.id)).distinct()
        return tasks
        
class UserProfile(APIView):
    """
    USER Profile detail view.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        application = Application.objects.get(client_id=settings.OAUTH2_CLIENT_ID)
        is_owner = False
        if application.user == request.user:
            is_owner = True
        data = {
            "username"  : request.user.username,
            "email"     : request.user.email,
            "id"        : request.user.id,
            "is_owner"  : is_owner,
        }
        return Response(data)

class LoginAPIView(APIView):
    """
    Login api view.
    """
    permission_classes = []

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = {
                'grant_type': 'password',
                'username': serializer.data['username'],
                'password': serializer.data['password']
            }

            login_response = requests.post('http://localhost:7000/o/token/', data=data, auth=(settings.OAUTH2_CLIENT_ID, settings.OAUTH2_CLIENT_SECRET))
            login_res_data = login_response.json()
            if login_response.status_code == 200:

                headers = {
                    'Authorization': '{} {}'.format(login_res_data['token_type'], login_res_data['access_token']),
                }

                response = requests.get('http://localhost:7000/user_profile/', headers=headers)
                user_profile_data = response.json()
                
                tasks = Task.objects.filter(Q(created_by=user_profile_data['id'])|Q(assigned_to=user_profile_data['id']))
                data = {
                    'status':   200,
                    'id'  : user_profile_data['id'],
                    'username'  : user_profile_data['username'],
                    'email'     : user_profile_data['email'],
                    'is_owner'  : user_profile_data['is_owner'],
                    'access_token': login_res_data['access_token'],
                    'token_type': login_res_data['token_type'],
                    'refresh_token': login_res_data['refresh_token'],
                }
                return Response(data)
            data = {
                'status': 403,
                'message': 'Error occured while login.'
            }
            return Response(data)
        return Response(serializer.errors)

class RegisterAPIView(APIView):
    """
    Register api view.
    """
    permission_classes = []

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():

            register_response = requests.post('http://localhost:7000/users/rest-auth/registration/', data=serializer.data)
            register_res_data = register_response.json()
            return Response(register_res_data)
        return Response(serializer.errors)

# NORMAL VIEWS
def login_view(request):
    """
    Login Form view.
    """
    form = LoginForm()
    return render(request, 'dashboard/login.html',{'form':form})

def register_view(request):
    """
    Register Form view.
    """
    form = UserCreationForm()
    return render(request, 'dashboard/register.html',{'form':form})

def dashboard(request):
    """
    Dashboard view.
    """
    form = TaskCreationForm()
    return render(request, 'dashboard/dashboard.html',{'form':form})

