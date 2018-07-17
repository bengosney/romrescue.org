from django.contrib.auth.models import User, Group
from .models import Dog
from rest_framework import serializers


class DogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dog
        fields = ('name', 'age', 'gender', 'raw_description')
