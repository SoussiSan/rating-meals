from django.shortcuts import render
from .models import Meal, Rating
from rest_framework import viewsets
from .serializers import MealSerializer, RatingSerializer


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
