from rest_framework import viewsets
from basic import models, serializers, queries


# class EmployeeViewSet(viewsets.ModelViewSet):
#     # queryset = models.Employee.objects.alias()
#     queryset = queries.exercicio3()
#     serializer_class = serializers.EmployeeSerializer

    # def list(self, request, *args, **kwargs):
    #     self.queryset = queries.exercicio3()
    #     return super(EmployeeViewSet, self).list(request, *args, **kwargs)


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer

    # def create(self, request, *args, **kwargs):  # POST
    #     return super(ZoneViewSet, self).create(request, *args, **kwargs)
    #
    # def partial_update(self, request, *args, **kwargs):  # PATCH
    #     return super(ZoneViewSet, self).partial_update(request, *args, **kwargs)
    #
    # def list(self, request, *args, **kwargs):  # GET
    #     return super(ZoneViewSet, self).list(request, *args, **kwargs)
    #
    # def retrieve(self, request, *args, **kwargs):  # GET/{parameter
    #     return super(ZoneViewSet, self).retrieve(request, *args, **kwargs)
    #
    # def destroy(self, request, *args, **kwargs):  # DELETE
    #     return super(ZoneViewSet, self).destroy(request, *args, **kwargs)


class MaritalStatusViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class StateViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.StateSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.SupplierSerializer


class ProductGroupViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.ProductGroupSerializer
