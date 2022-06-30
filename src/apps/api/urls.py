from rest_framework.routers import DefaultRouter

from .views import ClientReadOnlyViewSet


router = DefaultRouter()
router.register('clients', ClientReadOnlyViewSet, basename='clients')


urlpatterns = router.urls
