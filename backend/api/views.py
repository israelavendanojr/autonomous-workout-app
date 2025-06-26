from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    # Here list of all diff objs when creating new one
    queryset = User.objects.all()
    # Tells view what data we need to accept
    serializer_class = UserSerializer
    # Who can actually call this
    permission_classes = (AllowAny,)