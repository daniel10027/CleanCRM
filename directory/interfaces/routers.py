from rest_framework.routers import DefaultRouter
from .views import DirectoryViewSet

router = DefaultRouter()
router.register(r"directories", DirectoryViewSet, basename="directory")
urlpatterns = router.urls