from kombu.exceptions import OperationalError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from basic import models, serializers, queries, helpers, serializers_results, serializers_params, filters, tasks


# class EmployeeViewSet(viewsets.ModelViewSet):
#     # queryset = models.Employee.objects.alias()
#     queryset = queries.exercicio3()
#     serializer_class = serializers.EmployeeSerializer

    # def list(self, request, *args, **kwargs):
    #     self.queryset = queries.exercicio3()
    #     return super(EmployeeViewSet, self).list(request, *args, **kwargs)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    fiter_class = filters.EmployeeFilter

    @action(methods=['PATCH'], detail=True)
    def up_percentual(self, request, *args, **kwargs):
        percentual = request.data['percentual']

        if (percentual):
            employee = self.get_object()
            employee.adjustment_salary(percentual)
            employee.save()

            result = self.get_serializer(instance=employee, context=self.get_serializer_context())
            return Response(data=result.data, status=200)


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    filter_class = filters.ZoneFilter
    ordering_fields = '__all__'
    ordering = ('-id',)

    # @action(methods=['GET'], detail=False)
    # def get_by_name(self, request, *args, **kwargs):
    #     # name = request.query_params.get('name')
    #     result = serializers_params.ZoneGetByNameSerializer(data=request.query_params, context={'request': request})
    #     result.is_valid(raise_exception=True)
    #     #queryset = models.Zone.objects.filter(name__icontains=name)
    #     self.queryset = self.queryset.filter(name__icontains=result.validated_data.get('name'))
    #     return super(ZoneViewSet, self).list(request, *args, **kwargs)
    #     # result = serializers.ZoneSerializer(instance=self.queryset, many=True, context=self.get_serializer_context())
    #     # return Response(data=result.data, status=200)

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
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer

    # sobre escrevendo o list informando a relação inversa prefetch related (um para muitos)
    # pra evitar multiplas consultas
    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.prefetch_related('product_set')
        return super(SupplierViewSet, self).list(request, *args, **kwargs)


class ProductGroupViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.ProductGroupSerializer


class SaleModelViewSet(viewsets.ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = serializers.SaleSerializer

    @action(methods=['GET'], detail=False)
    def total_by_year(self, request, *args, **kwargs):
        try:
            tasks.sale_by_year.apply_async()
        except OperationalError as error:
            raise Exception(f'Broker connection error {error}')
        return Response(status=200)

        # result = serializers_results.SaleTotalByYearSerializer(
        #     instance=queryset,
        #     many=True,
        #     context=self.get_serializer_context()
        # )

        # queryset = helpers.execute_query(
        #     query=f"""
        #         SELECT EXTRACT('year' FROM s.date) AS year,
        #             EXTRACT('month' FROM s.date) AS month,
        #             SUM(p.sale_price * si.quantity) AS total
        #         FROM sale s
        #             INNER JOIN sale_item si ON s.id = si.id_sale
        #             INNER JOIN product p ON si.id_product = p.id
        #         GROUP BY EXTRACT('year' FROM s.date), EXTRACT('month', FROM s.date)
        #         ORDER BY EXTRACT('year' FROM s.date) DESC, EXTRACT('month' FROM s,date) DESC
        #     """
        # )


class ProductModelViewSet(viewsets.ModelViewSet):
    # colocando o select related para todas as consultas
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_class = filters.ProductFilter

    def list(self, request, *args, **kwargs):

        expand = request.query_params.get('expand', None)
        if expand is not None:
            relations = expand.split(',')
            for r in relations:
                self.queryset = self.queryset.select_related(r)
        return super(ProductModelViewSet, self).list(request, *args, **kwargs)


    # sobre-escrevendo o metodo list e passando o select_related para que django
    # faça a consulta correta com inner join, ao invés de fazer uma nova consulta para
    # cada item da lista
    # def list(self, request, *args, **kwargs):
    #     self.queryset = self.queryset.select_related('supplier')
    #     self.serializer_class = serializers.ProductListSerializer
    #     return super(ProductModelViewSet, self).list(request, *args, **kwargs)
    
    # fazendo a mesma coisa sobre escrevendo o retrieve (get by id)
    # def retrieve(self, request, *args, **kwargs):
    #     self.queryset = self.queryset.select_related('supplier')
    #     return super(ProductModelViewSet, self).retrieve(request, *args, **kwargs)
    


