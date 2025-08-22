from dataclasses import dataclass
from campaigns.infrastructure.models import Campaign, CampaignDelivery
from contacts.infrastructure.models import Contact
from notifications.infrastructure.email_impl import DjangoEmailSender
from notifications.infrastructure.console_sms import ConsoleSMSSender
from notifications.infrastructure.console_whatsapp import ConsoleWhatsAppSender
from app.celery import app

@dataclass
class CreateCampaignUseCase:
    def execute(self, *, name: str, channel: str, body: str, directory_id: int, subject: str | None = None) -> Campaign:
        return Campaign.objects.create(name=name, channel=channel, body=body, directory_id=directory_id, subject=subject)

@dataclass
class QueueDeliveriesUseCase:
    campaign_id: int
    def execute(self) -> int:
        camp = Campaign.objects.get(id=self.campaign_id)
        contacts = Contact.objects.filter(directory_id=camp.directory_id)
        created = 0
        for c in contacts:
            dest = (c.email if camp.channel == "email" else c.phone) or ""
            if not dest:
                continue
            d = CampaignDelivery.objects.create(campaign=camp, contact_id=c.id, destination=dest)
            send_campaign_delivery.delay(d.id)
            created += 1
        return created

@app.task
def send_campaign_delivery(delivery_id: int):
    d = CampaignDelivery.objects.get(id=delivery_id)
    camp = d.campaign
    try:
        if camp.channel == "email":
            DjangoEmailSender().send(d.destination, camp.subject or camp.name, camp.body)
        elif camp.channel == "sms":
            ConsoleSMSSender().send(d.destination, camp.body)
        else:
            ConsoleWhatsAppSender().send(d.destination, camp.body)
        d.status = "sent"
        d.save(update_fields=["status"])
    except Exception as e:
        d.status = "failed"
        d.error = str(e)
        d.save(update_fields=["status","error"])