from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from .models import Vacancy, Category, User, Resume
from .serializers import VacancySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.forms.models import model_to_dict
from django.db.models import Q


# Create your views here.
class VacancyPaginator(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 100


class VacancyAPIListByCategory(generics.ListAPIView):
    serializer_class = VacancySerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Vacancy.objects.filter(category__title=category)


#  Filtering by url params
# Q queries
class VacancyAPIListFilter(generics.ListAPIView):
    serializer_class = VacancySerializer

    def get_queryset(self):
        queryset = Vacancy.objects.all()
        min = self.request.query_params.get('min-bounty')
        max = self.request.query_params.get('max-bounty')
        q = self.request.query_params.get('q')
        # category = self.request.query_params.get('categories')

        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) & Q(maxBounty__lte=max) & Q(minBounty__gte=min))

        return queryset


# Filtering by user
class VacancyAPICurrentUserList(generics.ListAPIView):
    serializer_class = VacancySerializer
    pagination_class = VacancyPaginator

    def get_queryset(self):
        user = self.request.user
        return Vacancy.objects.filter(owner=user)


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = VacancyPaginator

    @action(methods=['get'], detail=False)
    def categories(self, request):
        cats = Category.objects.all()
        return Response({'categories': [c.title for c in cats]})

    @action(methods=['get'], detail=True)
    def resume(self, request, pk):
        user = self.request.user
        vacancy = Vacancy.objects.get(pk=pk)
        resume = Resume(vacancy=vacancy, user=user)
        resume.save()
        return Response({'vacancy': model_to_dict(vacancy), 'user': model_to_dict(user)})
