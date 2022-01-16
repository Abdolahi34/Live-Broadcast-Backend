from rest_framework import viewsets
from .serializers import ProgramSerializers
from Programs.models import Program

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()  # TODO order_by()
    serializer_class = ProgramSerializers