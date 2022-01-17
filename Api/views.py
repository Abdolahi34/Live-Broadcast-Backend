from rest_framework import viewsets
from .serializers import ProgramSerializers
from Programs.models import Program


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all().order_by('slug')
    serializer_class = ProgramSerializers