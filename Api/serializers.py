from rest_framework import serializers
from Programs.models import Program


class ProgramSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


