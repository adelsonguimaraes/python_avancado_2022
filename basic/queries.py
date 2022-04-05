from django.db.models import Value, ExpressionWrapper, F, IntegerField, FloatField, Q, DateField, DurationField, Case, \
    When, CharField, Sum, Max, Min, Avg, Count, OuterRef, Subquery, Exists
from django.db.models.functions import Now, Cast, ExtractDay, LPad, Upper, Lower

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
        tempo_casa = ExpressionWrapper(
            F('admission_date') - Now(), output_field=DurationField(),
        )
    ).values(
            'name', 'tempo_casa'
    )


def exercicio13():
    # pegar o id e adicionar 5 zeros a esquerda
    return models.Employee.objects.annotate(
        code=LPad(
                Cast(F('id'), output_field=CharField()),
                5, Value('0')
            )
        ).values('code', 'id', 'name')


def exercicio14():
    return models.Employee.objects.annotate(
        _upper=Upper('name'),
        _lower=Lower('name')
    ).values('_upper', '_lower')


def exercicio15():
    return models.Employee.objects.select_related('department').values('department__name', 'gender').annotate(
        sum=Sum('salary')
    ).values('department__name', 'sum', 'gender')


# Fazer uma consulta para retornar o nome do produto, subtotal e quanto deve ser pago de comissão por cada item;
# Fazer uma consulta para retornar o nome do produto, subtotal e quanto foi obtido de lucro por item;
# Ranking dos 10 funcionários mais bem pagos;
# Ranking dos 20 clientes que tem a menor renda mensal;
# Trazer do décimo primeiro ao vigésimo funcionário mais bem pago;
# Ranking dos produtos mais caros vendidos no ano de 2021;
# Criar uma consulta para trazer o primeiro nome dos funcionários.
#     Sr. Sra. Dr. Dra. remover se tiver.
# Criar uma consulta para trazer o último nome dos clientes.
# Criar uma consulta para rocar quem tenha silva no nome para Oliveira.
# Criar uma consulta para trazer o total de funcionários por estado civil;
# Criar uma consulta para trazer o total vendido em valor R$ por zona;
# Criar uma consulta para trazer o total vendido em valor R$ por estado;
# Criar uma consulta para trazer o total vendido em quantidade por cidade, trazer apenas as cidades que tiveram vendas acima de quantidade 100;
# Trazer a media de salários por sexo, o sexo deve está de forma descritiva;
# Fazer uma consulta que retorne os 5 grupos de produtos mais lucrativos em termos de valor, os grupos só entram na lista com lucros acima de R$ 200,00;
# Uma consulta para trazer a média de salários por departamento;
# Uma consulta para trazer o total vendido em valor por ano;
# Uma consulta para trazer o total vendido em valor por idade de funcionário;


def exercicio16():
    # Fazer uma consulta para retornar o nome do funcionário e o bairro onde ele mora;
    return models.Employee.objects.select_related('district').values('name', 'district__name')


def exercicio17():
    # Fazer uma consulta para retornar o nome do cliente, cidade e zona que o mesmo mora;
    return models.Customer.objects.values(
        'name', 'district__customer__name', 'district__zone__name'
    )

def exercicio18():
    # Fazer uma consulta para retornar os dados da filial, estado e cidade onde a mesma está localizada;
    return models.Branch.objects.values(
        'name', 'district__name', 'district__city__state__name', 'district__city__name'
    )


def exercicio19():
    # Fazer uma consulta par retornar os dados do funcionário, departamento onde ele trabalha e qual seu estado civil atual;
    return models.Employee.objects.values(
        'name', 'department__name', 'marital_status__name'
    )


def exercicio20():
    # Fazer uma consulta para retornar o nome do produto vendido, o preço unitário e o subtotal;
    return models.SaleItem.objects.annotate(
        subtotal = ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField())
    ).values(
        'product__name', 'product__sale_price', 'subtotal'
    )


def exercicio21(commission=True):
    field = 'product__product_group__commission_percentage'
    if not commission:
        field = 'product__product_group__gain_percentage'
    return models.SaleItem.objects.select_related('product__product_group').annotate(
        subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField()),
        commission_or_gain=ExpressionWrapper(
            F('subtotal') * (F(field) / 100),
            output_field=FloatField()
        )
    ).values(
        'product__name', 'product__sale_price', 'subtotal',
        'product__product_group__commission_percentage',
        'commission_or_gain'
    )


def exercicio25():
    # Criar uma consulta para trazer o total vendido em valor R$ por zona
    return models.SaleItem.objects.select_related('sale__branch__district__zone').values(
        'sale__branch__district__zone__name'
    ).annotate(
        total=Sum(ExpressionWrapper(
            F('quantity') * F('product__sale_price'), output_field=FloatField()
        ))
    ).values('sale__branch__district__zone__name', 'total')


def exercicio26():
    # Criar uma consulta para trazer o total vendido em valor R$ por filial;
    return models.SaleItem.objects.select_related('sale__branch').values(
        'sale__branch__district__zone__name'
    ).annotate(
        total=Sum(ExpressionWrapper(
            F('quantity') * F('product__sale_price'), output_field=FloatField()
        ))
    ).values('sale__branch__name', 'total')


def exercicio27():
    # Criar uma consulta para trazer o total de funcionários por estado civil;
    return models.Employee.objects.values('marital_status__name').annotate(
        total=Count(F('id'))
    ).values(
        'marital_status__name', 'total'
    )


def exercicio28():
    # Criar uma consulta para trazer o total vendido em valor R$ por estado;
    return models.SaleItem.objects.values('sale__branch__district__city__state__name').annotate(
        total=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField())
    ).values(
        'sale__branch__district__city__state__name', 'total'
    )


def exercicio29():
    # Uma consulta para trazer o total vendido em valor por ano;
    return models.SaleItem.objects.values(
        'sale__date__year'
    ).annotate(
        total=Sum(ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField()))
    ).values(
        'sale__date__year', 'total'
    )


def exercicio30():
    # subquery
    sbq = models.SaleItem.objects.select_related('sale').filter(
        product=OuterRef('id')
    ).values('sale__date').order_by('-sale__date')[:1]
    return models.Product.objects.annotate(last_sale=Subquery(sbq)).values('id', 'name', 'last_sale')


def exercicio31():
    sbq = models.SaleItem.objects.filter(product=OuterRef('id'), sale__date__year=2021)[:1]
    return models.Product.objects.annotate(
        exists=Exists(sbq)
    ).values('id', 'name', 'exists')


def exercicio32():
    # flat True retorna apenas os valores sem chave
    # distinct remove os duplicados
    sbq = models.SaleItem.objects.filter(sale__date__year=2021).values_list('product', flat=True).distinct()
    # usando o IN no id e passando a subquery
    return models.Product.objects.filter(id__in=sbq).values('id', 'name')


def max():
    # pega o salário de maior valor
    return  models.Employee.objects.aggregate(max=Max('salary'))

def min():
    # pega o sário de minimo valor
    return models.Employee.objects.aggregate(max=Min('salary'))

def avg():
    # pega a media
    return models.Employee.objects.aggregate(max=Avg('salary'))

def sum():
    # soma todos os salarios
    return models.Employee.objects.aggregate(max=Sum('salary'))

def count():
    # conta todos os itens
    return models.Employee.objects.aggregate(max=Count('*'))