from django.shortcuts import render
from rest_framework import generics
from .models import Vacancy
from .serializers import VacancySerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

# class VacancyAPIView(generics.ListAPIView):
#     queryset = Vacancy.objects.all()
#     serializer_class = VacancySerializer

class VacancyAPIView(APIView):
    def get(self, request):
        return Response({'title': 'asd'})