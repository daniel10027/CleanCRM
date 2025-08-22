from dataclasses import dataclass
from typing import Iterable
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdfcanvas
from contacts.infrastructure.models import Contact

@dataclass
class ImportContactsUseCase:
    directory_id: int
    def execute(self, file_obj) -> int:
        """Import CSV/XLSX vers Contact. Colonnes: first_name,last_name,email,phone"""
        df = pd.read_excel(file_obj) if str(getattr(file_obj, 'name','')).endswith('xlsx') else pd.read_csv(file_obj)
        created = 0
        for _, row in df.iterrows():
            Contact.objects.create(
                directory_id=self.directory_id,
                first_name=row.get('first_name'),
                last_name=row.get('last_name'),
                email=row.get('email'),
                phone=str(row.get('phone') or "")
            )
            created += 1
        return created

@dataclass
class ExportContactsUseCase:
    directory_id: int
    def to_csv(self) -> bytes:
        qs = Contact.objects.filter(directory_id=self.directory_id).values(
            'first_name','last_name','email','phone'
        )
        import csv
        from io import StringIO
        s = StringIO()
        writer = csv.DictWriter(s, fieldnames=['first_name','last_name','email','phone'])
        writer.writeheader()
        for row in qs:
            writer.writerow(row)
        return s.getvalue().encode()

    def to_xlsx(self) -> bytes:
        qs = list(Contact.objects.filter(directory_id=self.directory_id).values(
            'first_name','last_name','email','phone'
        ))
        import pandas as pd
        from io import BytesIO
        buf = BytesIO()
        pd.DataFrame(qs).to_excel(buf, index=False)
        return buf.getvalue()

    def to_pdf(self) -> bytes:
        qs = list(Contact.objects.filter(directory_id=self.directory_id).values_list(
            'first_name','last_name','email','phone'
        ))
        buf = BytesIO()
        c = pdfcanvas.Canvas(buf, pagesize=A4)
        width, height = A4
        y = height - 50
        c.setFont("Helvetica", 12)
        c.drawString(50, y, "Contacts")
        y -= 30
        for fn, ln, email, phone in qs:
            line = f"{fn or ''} {ln or ''} | {email or ''} | {phone or ''}"
            c.drawString(50, y, line)
            y -= 18
            if y < 50:
                c.showPage(); y = height - 50
        c.save()
        return buf.getvalue()