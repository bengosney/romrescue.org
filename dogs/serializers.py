# Third Party
from rest_framework import serializers

# First Party
from dogs.models import Dog


class DogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dog
        fields = ("name", "age", "gender", "raw_description")
