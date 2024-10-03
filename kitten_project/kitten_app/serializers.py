from rest_framework import serializers
from .models import Kitten, Breed, Rating

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'

class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = ['id', 'color', 'age', 'description', 'breed', 'owner']
        read_only_fields = ['owner']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'kitten', 'score']
        read_only_fields = ['user']
