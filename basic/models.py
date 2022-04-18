from decimal import Decimal
from django.db import models
from basic import managers


# Create your models here.
class ModelBase(models.Model):
    class Gender(models.TextChoices):
        MALE = ('M', 'Male')
        FEMALE = ('F', 'Female')

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, auto_now=True)
    active = models.BooleanField(null=False, default=True)

    class Meta:
        abstract = True


class Department(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)

    class Meta:
        db_table = 'department'
        managed = True

    def __str__(self):
        return self.name


class Zone(ModelBase):
    name = models.CharField(max_length=64, null=False)

    class Meta:
        db_table = 'zone'
        managed = True

    def __str__(self):
        return self.name


class District(ModelBase):
    name = models.CharField(max_length=64, null=False, default='')
    city = models.ForeignKey(
        to='city',
        on_delete=models.DO_NOTHING,
        db_column='id_city',
        null=False
    )
    zone = models.ForeignKey(
        to='Zone',
        on_delete=models.DO_NOTHING,
        db_column='id_zone',
        null=False
    )

    class Meta:
        db_table = 'district'
        managed = True

    def __str__(self):
        return self.name


class City(ModelBase):
    state = models.ForeignKey(
        to='State',
        on_delete=models.DO_NOTHING,
        db_column='id_state',
        null=False
    )
    name = models.CharField(max_length=64, null=False)

    class Meta:
        db_table = 'city'
        managed = True

    def __str__(self):
        return f'{self.name} - {self.state}'


class State(ModelBase):
    name = models.CharField(max_length=64, null=False)
    abbreviation = models.CharField(max_length=2, null=False)

    class Meta:
        db_table = 'state'
        managed = True

    def __str__(self):
        return f'{self.name} - {self.abbreviation}'


class Supplier(ModelBase):
    name = models.CharField(max_length=64, null=False)
    legal_document = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'supplier'
        managed = True


class ProductGroup(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    gain_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=False)

    class Meta:
        db_table = 'product_group'
        managed = True


class Customer(ModelBase):
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        db_column='id_marital_status',
        null=False
    )
    name = models.CharField(max_length=64, null=False)
    income = models.DecimalField(max_digits=16, decimal_places=2, null=False)
    gender = models.CharField(max_length=10, null=False, choices=ModelBase.Gender.choices)

    class Meta:
        db_table = 'customer'
        managed = True

    def __str__(self):
        return self.name


class Branch(ModelBase):
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False
    )
    name = models.CharField(max_length=64, null=False, unique=True)

    class Meta:
        db_table = 'branch'
        managed = True


class Sale(ModelBase):
    customer = models.ForeignKey(
        to='Customer',
        on_delete=models.DO_NOTHING,
        db_column='id_customer',
        null=False
    )
    branch = models.ForeignKey(
        to='Branch',
        on_delete=models.DO_NOTHING,
        db_column='id_branch',
        null=False
    )
    employee = models.ForeignKey(
        to='Employee',
        on_delete=models.DO_NOTHING,
        db_column='id_employee',
        null=False
    )
    date = models.DateTimeField(null=False)
    objects = managers.SaleManager()

    class Meta:
        db_table = 'sale'
        managed = True


class SaleItem(ModelBase):
    sale = models.ForeignKey(
        to='Sale',
        on_delete=models.DO_NOTHING,
        db_column='id_sale',
        null=False
    )
    product = models.ForeignKey(
        to='Product',
        on_delete=models.DO_NOTHING,
        db_column='id_product',
        null=False
    )
    quantity = models.DecimalField(max_digits=16, decimal_places=3, null=False)
    sale_price = models.DecimalField(max_digits=16, decimal_places=2, null=False, default=0)

    class Meta:
        db_table = 'sale_item'
        managed = True


class Product(ModelBase):
    product_group = models.ForeignKey(
        to='ProductGroup',
        on_delete=models.DO_NOTHING,
        db_column='id_product_group',
        null=False
    )
    supplier = models.ForeignKey(
        to='Supplier',
        on_delete=models.DO_NOTHING,
        db_column='id_supplier',
        null=False
    )
    name = models.CharField(max_length=64, null=False, unique=True)
    cost_price = models.DecimalField(max_digits=16, decimal_places=2, null=False)
    sale_price = models.DecimalField(max_digits=16, decimal_places=2, null=False)

    class Meta:
        db_table = 'product'
        managed = True


class MaritalStatus(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)

    class Meta:
        db_table = 'marital_status'
        managed = True

    def __str__(self):
        return self.name


class Employee(ModelBase):
    name = models.CharField(max_length=100, null=False)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    gender = models.CharField(max_length=1, null=False, choices=ModelBase.Gender.choices)
    admission_date = models.DateField(null=False)
    birth_date = models.DateField(null=False)
    department = models.ForeignKey(
        to="Department",
        on_delete=models.DO_NOTHING,
        db_column='id_department',
        null=False,
        default=1
    )
    district = models.ForeignKey(
        to="District",
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False,
        default=1,
        related_name='employees'
    )
    marital_status = models.ForeignKey(
        to="MaritalStatus",
        on_delete=models.DO_NOTHING,
        db_column='id_marital_status',
        null=False,
        default=1
    )

    class Meta:
        db_table = 'employee'
        managed = True

    def __str__(self):
        return self.name

    def adjustment_salary(self, percent):
        self.salary += self.salary * (Decimal(percent)/100)
