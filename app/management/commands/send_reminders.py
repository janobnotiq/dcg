from app.models import Declaration  # Modelingizni import qiling
from app.utils import prepare_message, send_message

from django.core.management.base import BaseCommand
from django.db.models import Q

from time import sleep

class Command(BaseCommand):
    help = "Bot orqali deklaratsiyalar haqida eslatma yuboradi"

    def handle(self, *args, **kwargs):
        # Barcha deklaratsiyalarni oling
        declarations = Declaration.objects.filter(
            Q(customs_mode=Declaration.Modes.ND40) | Q(customs_mode=Declaration.Modes.IM70)
)
        print(declarations)
        for declaration in declarations:
            if declaration.days_left % 10 != 0:
                continue
            
            try:
                message = prepare_message(declaration)
                print(message)
            except ValueError:
                continue
            
            send_message(message)
            sleep(5)
        
