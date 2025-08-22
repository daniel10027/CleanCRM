from django.core.mail import send_mail
from django.conf import settings

class DjangoEmailSender:
    def send(self, to_email: str, subject: str, body: str) -> None:
        send_mail(subject or "", body, settings.DEFAULT_FROM_EMAIL, [to_email], fail_silently=False)