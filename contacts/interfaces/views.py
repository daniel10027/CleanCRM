from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contacts.infrastructure.models import Contact
from .serializers import ContactSerializer
from contacts.application.use_cases import ImportContactsUseCase, ExportContactsUseCase
from django.http import HttpResponse

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        directory_id = self.request.query_params.get('directory')
        qs = Contact.objects.all()
        if directory_id:
            qs = qs.filter(directory_id=directory_id)
        return qs

    @action(detail=False, methods=["post"], url_path="import")
    def import_contacts(self, request):
        directory_id = int(request.data.get("directory_id"))
        f = request.FILES.get("file")
        created = ImportContactsUseCase(directory_id).execute(f)
        return Response({"created": created})

    @action(detail=False, methods=["get"], url_path="export")
    def export_contacts(self, request):
        directory_id = int(request.query_params.get("directory_id"))
        fmt = request.query_params.get("format", "csv")
        uc = ExportContactsUseCase(directory_id)
        if fmt == "xlsx":
            data, ct, name = uc.to_xlsx(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "contacts.xlsx"
        elif fmt == "pdf":
            data, ct, name = uc.to_pdf(), "application/pdf", "contacts.pdf"
        else:
            data, ct, name = uc.to_csv(), "text/csv", "contacts.csv"
        resp = HttpResponse(data, content_type=ct)
        resp["Content-Disposition"] = f"attachment; filename={name}"
        return resp