from __future__ import absolute_import, unicode_literals
import os
from root.celery import Celery
from celery.schedules import crontab  # Cron jadvali uchun

# Django settings faylini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DCG.root.settings')

app = Celery('root')

# Django settings dan Celery sozlamalarini yuklash
app.config_from_object('django.conf:settings', namespace='CELERY')

# Task'larni avtomatik topish
app.autodiscover_tasks()

# Periodik tasklar jadvali
app.conf.beat_schedule = {
    'check-declarations-every-day-22-30': {
        'task': 'app.tasks.check_declarations',  # Taskning yo'li
        'schedule': crontab(minute=30, hour=22),  # Har kuni soat 22:30 da
    },
}
