from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from .models import Profile
from rest_framework import viewsets
from userprofile.serializers import *


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by('birth_date')
    serializer_class = UserProfileSerializer
    lookup_field = 'slug'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
