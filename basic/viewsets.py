from rest_framework import viewsets
from basic import models, serializers, queries


class EmployeeViewSet(viewsets.ModelViewSet):
    # queryset = models.Employee.objects.alias()
    queryset = queries.exercicio3()
    serializer_class = serializers.EmployeeSerializer

    # def list(self, request, *args, **kwargs):
    #     self.queryset = queries.exercicio3()
    #     return super(EmployeeViewSet, self).list(request, *args, **kwargs)
