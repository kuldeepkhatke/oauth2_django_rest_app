from rest_framework import generics

from django.contrib.auth.models import User
from . import models
from . import serializers

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer