from celery import shared_task
import requests
import datetime
from dotenv import load_dotenv
from .models import Declaration
import os
from django.db.models import Q

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("GROUP_CHAT_ID")

def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Xabar yuborildi")
    else:
        print(f"Xatolik: {response.text}")

@shared_task
def check_declarations():
    current_date = datetime.date.today()
    declarations = Declaration.objects.filter(
        Q(customs_mode=Declaration.Modes.ND40) | Q(customs_mode=Declaration.Modes.IM70)
        )
    for declaration in declarations:
            if declaration.left_days() is not None:
                send_message(declaration.left_days())
