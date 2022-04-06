from rest_framework import serializers

from basic import models


# class EmployeeSerializer(serializers.Serializer):
#     name = serializers.CharField(read_only=True)
#     district = serializers.CharField(read_only=True, source='district__name')
#     city = serializers.CharField(read_only=True, source='district__city__name')
#     state = serializers.CharField(read_only=True, source='district__city__state__name')

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Zone
        fields = '__all__'

    def validate(self, attrs):
        if not attrs.get('nome').isupper():
            raise Exception('O nome deve ser uppercase')
        return super(ZoneSerializer, self).validate(attrs)
#
#     def create(self, validated_data):
#         return super(ZoneSerializer, self).create(validated_data)
#
#     def update(self, instance, validated_data):
#         return super(ZoneSerializer, self).update(instance, validated_data)
#
#     def to_representation(self, instance):
#         data = super(ZoneSerializer, self).to_representation(instance)
#         data['campo_calculado'] = 10 * 10
#         return data


# class ZoneSeializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     create_at = serializers.DateTimeField(read_only=True)
#     modified_at = serializers.DateTimeField(read_only=True)
#     active = serializers.BooleanField(required=False)
#     name = serializers.CharField(required=True, max_length=64)
#
#     # def validators(self, attrs):
#     #     return super(ZoneSeializer, self).validate(attrs)
#
#     def create(self, validated_data):
#         return models.Zone.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         instance.save()
#         return instance
#
#     def to_representation(self, instance):
#         return super(ZoneSeializer, self).to_representation(instance)


class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaritalStatus
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supplier
        fields = '__all__'


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductGroup
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sale
        fields = '__all__'


