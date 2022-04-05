from rest_framework.routers import DefaultRouter
from basic import viewsets


router = DefaultRouter()
# router.register('employee', viewsets.EmployeeViewSet)
router.register('zone', viewsets.ZoneViewSet)
router.register('marital_status', viewsets.MaritalStatusViewSet)
router.register('department', viewsets.DepartmentViewSet)
router.register('state', viewsets.StateViewSet)
router.register('supplier', viewsets.SupplierViewSet)
router.register('product_group', viewsets.ProductGroupViewSet)

urlpatterns = router.urls
