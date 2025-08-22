from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, CampaignDeliveryViewSet

router = DefaultRouter()
router.register(r"campaigns", CampaignViewSet, basename="campaign")
router.register(r"deliveries", CampaignDeliveryViewSet, basename="delivery")
urlpatterns = router.urls