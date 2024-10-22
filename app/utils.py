import os
import requests
from app.models import Declaration  


TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("GROUP_CHAT_ID")

def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Xabar yuborildi")
    else:
        print(f"Xatolik: {response.text}")

def prepare_message(declaration:Declaration) -> str:
    first_name = ""
    last_name = ""
    username = ""
    number_gtd = None
    days_left = getattr(declaration,"days_left",None)

    if declaration.declarant and declaration.declarant.first_name:
        first_name = declaration.declarant.first_name

    if declaration.declarant and declaration.declarant.last_name:
        last_name = declaration.declarant.last_name

    if declaration.declarant and declaration.declarant.username:
        username = declaration.declarant.username

    if declaration.number_gtd:
        number_gtd = declaration.number_gtd
   
    if not all([number_gtd, days_left]):
        raise ValueError

    message = f"🙂 Hurmatli {first_name} {last_name}! @{username} \n\n\
🚚 Sizning {number_gtd} raqamli deklaratsiyangiz boshqa rejimga olib o'tilishi kerak.\n\n\
📆 <b>{declaration.days_left}</b> kun qoldi⏳⌛\n\n\
🔗🔗🔗 Ushbu link orqali uni ko'rishingiz mumkin: http://127.0.0.1:8000/update-declaration/{declaration.pk}/ \n\n\
Ishlarga rivoj😉"
    
    return message