from django.db.models import Value, ExpressionWrapper, F, IntegerField, FloatField, Q, DateField, DurationField, Case, When
from django.db.models.functions import Now, Cast, ExtractDay

from basic import models


def utilizando_case():
    return models.Employee.objects.annotate(
        gender_description=Case(
            When(gender=models.ModelBase.Gender.MALE, then=Value('Masculino')),
            default=Value('Feminino')
        )
    )


def exercicio1():
    # Exercicio
    # Consulta paa retornar um status do funcionário de acordo com seu salário
    # até 2000 (Vendedor Jr)
    # maior que 2000 e menor ou igual a 5000 (Vendedor Pleno)
    # Acima de 5000 (Vendedor Sênior)

    return models.Employee.objects.annotate(
        office=Case(
            When(salary__lte=2000, then=Value('Vendedor Jr')),
            When(salary__gt=2000, salary__lte=5000, then=Value('Vendedor Pleno')),
            default=Value('Vendedor Sênior')
        )
    ).values('name', 'salary', 'office')


def exercicio2():
    return models.Employee.objects.annotate(
        bairro=F('district__name'),
        cidade=F('district__city__name'),
        estado=F('district__city__state__name')
    ).values('name', 'bairro', 'cidade', 'estado')


def exercicio3():
    return models.Employee.objects.values(
        'district__name',
        'district__city__name',
        'district__city__state__name'
    )


def exercicio4(qt):
    return models.Product.objects.annotate(
        subtotal=ExpressionWrapper(F('sale_price')*qt, output_field=FloatField()),
        commission=ExpressionWrapper(F('subtotal')*(F('product_group__commission_percentage')/100), output_field=FloatField())
    ).values('name', 'sale_price', 'subtotal', 'commission')

def exercicio5():
    # return models.Employee.objects.filter(
    #    Q(marital_status__name__icontains='casado') |
    #    Q(marital_status__name__icontains='solteiro')
    # )

    return models.Employee.objects.filter(
        marital_status__name__in=['Solteiro', 'Casado']
    )


def exercicio6():
    # Fazer uma consulta para retornar todos funcionarios casados ou solteiros
    return models.Employee.objects.filter(marital_status__name__in=('Solteiro', 'Casado')).values(
        'name', 'marital_status__name'
    )

def exercicio7():
    # Fazer uma consulta para retornar todos os funcionarios que ganham entre R$ 1.0000 e R$ 5.000
    return models.Employee.objects.filter(salary__range=(1000, 5000)).values(
        'name', 'salary'
    )


def exercicio8():
    # Fazer uma consulta que retorne a diferença do preço de custo e preço de venda dos produtos
    return models.Product.objects.annotate(
        diff=ExpressionWrapper(F('sale_price') - F('cost_price'), output_field=FloatField())
    ).values(
        'name', 'cost_price', 'sale_price', 'diff'
    )


def exercicio9():
    # Fazer uma consulta que retorne todos os funcionários que não tenham salário entre 4000 e 8000
    return models.Employee.objects.exclude(salary__range=(4000, 8000)).values(
        'name', 'salary'
    )


def exercicio10():
    # Fazer uma consulta para retornar todas as vendas entre 2010 e 2021
    return models.Sale.objects.filter(date__year__range=(2010, 2021)).values(
        'saleitem__product__name', 'date'
    )


def exercicio11():
    return models.Employee.objects.annotate(
        # diff=ExpressionWrapper(Cast(Now(), output_field=DateField()) - F('birth_date'), output_field=DurationField()),
        # age=ExpressionWrapper(ExtractDay(F('diff')) / 365, output_field=IntegerField()),
        age=ExpressionWrapper(2022-F('birth_date__year'), output_field=IntegerField()),
        tipo=Case(
            When(age__range=(18, 25), then=Value('Jr')),
            When(age__range=(26, 34), then=Value('Pleno')),
            When(age__gte=35, then=Value('Sẽnior')),
            default=Value('Menor Aprendiz')
        )
    ).values(
        'name', 'age', 'tipo'
    )


def exercicio12():
    # Fazer uma consulta que retorne o tipo de funcionario de acordo com o tempo de casa.
    # até 2 anos - Novato
    # Acima de 2 anos e menor ou igual a 5 anos - Intermediário
    # Acima de 5 anos - Veterano
    return models.Employee.objects.annotate(

    )

# def exercicio6():
#     # return models.Employee.objects.filter(salary__range=(1000, 5000))
#     return models.Employee.objects.filter(salary__gte=1000, sale__modified_at__gte=5000)
#
#
# def exercico7():
#     return models.Product.objects.annotate(
#         diff=ExpressionWrapper(F('sale_price') - F('cost_price'), output_field=FloatField())
#     ).values('name', 'sale_price', 'cost_price', 'diff')
#
#
# def exercicio8():
#     return models.Employee.objects.exclude(salary__range=(4000, 8000))
#
#
# def exercicio9():
#     return models.Sale.objects.filter(date__year__range=(2010, 2021))
#
#
# def exercici10():
#     return models.Employee.objects.annotate(
#         diff=ExpressionWrapper(Cast(Now(), output_field=DateField()) - F('birth_date'), output_field=DurationField())
#     )