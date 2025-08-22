from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from campaigns.infrastructure.models import Campaign, CampaignDelivery
from .serializers import CampaignSerializer, CampaignDeliverySerializer
from campaigns.application.use_cases import CreateCampaignUseCase, QueueDeliveriesUseCase

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all().order_by('-id')
    serializer_class = CampaignSerializer

    @action(detail=True, methods=["post"], url_path="queue")
    def queue(self, request, pk=None):
        uc = QueueDeliveriesUseCase(int(pk))
        count = uc.execute()
        return Response({"queued": count})

class CampaignDeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CampaignDelivery.objects.all().order_by('-id')
    serializer_class = CampaignDeliverySerializer