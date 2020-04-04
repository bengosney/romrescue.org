# Third Party
from rest_framework import serializers

# Locals
from .models import Dog


class DogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dog
        fields = ('name', 'age', 'gender', 'raw_description')
