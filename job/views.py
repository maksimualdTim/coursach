from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from .models import Vacancy, Category, Profile
from .serializers import VacancySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class VacancyPaginator(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 100


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = VacancyPaginator

    @action(methods=['get'], detail=False)
    def categories(self, request):
        cats = Category.objects.all()
        return Response({'categories': [c.title for c in cats]})

    # @action(methods=['post'], detail=True)
    # def owner(self, request, pk):
    #     objs = Profile.objects.filter(pk=pk)

# class VacancyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Vacancy.objects.all()
#     serializer_class = VacancySerializer
#
#
# class VacancyAPIViewList(generics.ListAPIView):
#     queryset = Vacancy.objects.all()
#     serializer_class = VacancySerializer
