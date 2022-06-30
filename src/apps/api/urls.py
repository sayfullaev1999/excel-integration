from rest_framework.routers import DefaultRouter

from .views import (
    BillReadOnlyViewSet,
    ClientReadOnlyViewSet,
)


router = DefaultRouter()
router.register('clients', ClientReadOnlyViewSet, basename='clients')
router.register('bills', BillReadOnlyViewSet, basename='bills')

urlpatterns = router.urls
