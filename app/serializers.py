from .models import Mouse
from rest_framework import serializers


class MouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mouse
        fields = ('mouse_id', 'dob', 'dod', 'status')
