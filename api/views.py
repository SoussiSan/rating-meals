from django.shortcuts import render
from .models import Meal, Rating
from rest_framework import viewsets, status
from .serializers import MealSerializer, RatingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            stars = request.data['stars']
            username = request.data['username']

            # 🧩 Check if user exists
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # 🧩 Check if meal exists
            try:
                meal = Meal.objects.get(id=pk)
            except Meal.DoesNotExist:
                return Response({'message': 'Meal not found'}, status=status.HTTP_404_NOT_FOUND)

            # 🧩 Create or update rating
            try:
                rating = Rating.objects.get(user=user, meal=meal)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                return Response({'message': 'Meal Rate Updated', 'result': serializer.data}, status=status.HTTP_200_OK)

            except Rating.DoesNotExist:
                rating = Rating.objects.create(user=user, meal=meal, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                return Response({'message': 'Meal Rate Created', 'result': serializer.data}, status=status.HTTP_201_CREATED)

        else:
            return Response({'message': 'stars not provided'}, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
