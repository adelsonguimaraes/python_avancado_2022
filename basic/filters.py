from django.db.models import Q, OuterRef, Exists
from django_filters import filterset
from django_filters.widgets import BooleanWidget
from basic import models


# criando um tipo de dado mixto, tipo IN + tipo Number
class NumberInFilter(filterset.BaseInFilter, filterset.NumberFilter):
    pass


# criando um tipo de dado mixto, tipo Range + tipo Number
class NumberRangeFilter(filterset.BaseRangeFilter, filterset.NumberFilter):
    pass


# criando um tipo de dado mixto, tipo IN + tipo Char
class CharInFilter(filterset.BaseInFilter, filterset.CharFilter):
    pass


class ZoneFilter(filterset.FilterSet):
    name = filterset.CharFilter(lookup_expr='icontains')
    active = filterset.BooleanFilter(widget=BooleanWidget)

    class Meta:
        model = models.Zone
        fields = ['name', 'active']


class EmployeeFilter(filterset.FilterSet):
    # filtro por nome ou departamento
    name_or_department = filterset.CharFilter(method='filter_name_or_department')

    # start_salary = filterset.NumberFilter(field_name='salary', lookup_expr='gte')
    # final_salary = filterset.NumberFilter(field_name='salary', lookup_expr='lte')
    # na url o parametro fica ?start_salary=100&final_salary=3000

    salary_range = NumberRangeFilter(field_name='salary', lookup_expr='range')
    # na url o parametro fica ?salary_range=1000,2000

    salary_in = NumberInFilter(field_name='salary', lookup_expr='in')
    # na url o parametro fica ?salary_in=1613,1914

    gender_in = CharInFilter(field_name='gender', lookup_expr='in')
    # na url o parametro fica ?gender_in=M,F

    def filter_name_or_department(self, queryset, name, value):
        # usando a queryset que vem da model pra fazer um filtro com OU usando Q() | Q()
        return queryset.filter(Q(name__icontains=value) | Q(department__name__icontains=value))
        # na url o parametro fica ?name_or_department=silva

    class Meta:
        model = models.Employee
        fields = ['salary_range', 'salary_in']


class ProductFilter(filterset.FilterSet):
    exists_sale = filterset.BooleanFilter(widget=BooleanWidget, method='filter_exists_sale')

    @staticmethod
    def filter_exists_sale(queryset, name, value):
        # subquery na tabela sale item por id de produto
        subquery = models.SaleItem.objects.filter(product=OuterRef('id'))
        # se existe venda (subquery) filtra
        return queryset.annotate(exists=Exists(subquery)).filter(exists=value)

    class Meta:
        model = models.Product
        fields = ['exists_sale']
