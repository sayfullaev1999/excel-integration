from rest_framework.routers import DefaultRouter

from .views import (
    BillReadOnlyViewSet,
    ClientReadOnlyViewSet,
    UploadFileView
)


router = DefaultRouter()
router.register('clients', ClientReadOnlyViewSet, basename='clients')
router.register('bills', BillReadOnlyViewSet, basename='bills')
router.register('upload', UploadFileView, basename='upload')

urlpatterns = router.urls
