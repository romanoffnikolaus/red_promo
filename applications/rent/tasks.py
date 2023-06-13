from datetime import date, timedelta

from django.core.mail import send_mail
from django.db.models import Count, Avg, F
from celery import shared_task

from .models import Rent
from applications.account.models import User


@shared_task
def debt_checking():
    current_date = date.today()
    two_weeks_ago = current_date - timedelta(days=14)
    debts = Rent.objects.filter(expiration_date__lte=two_weeks_ago)
    emails = list(User.objects.values_list('email', flat=True))
    for element in debts:
        book_title = element.book.title
        user = element.tenant.email
        message = f"Книга '{book_title}' не была возвращена после истечения срока аренды пользователем {user}."

        send_mail("Просроченная аренда", message, "red_promo@example.com", emails)


@shared_task
def daily_statistics():
    today = date.today()
    start_date = today - timedelta(days=1)
    book_stats = Rent.objects.filter(created_at__range=(start_date, today)).values('book__title').annotate(count=Count('book'), 
        avg_duration=Avg(F('expiration_date') - F('created_at')))

    message = "Статистика аренды книг за сутки:\n"
    for element in book_stats:
        title = element['book__title']
        count = element['count']
        avg_duration = element['avg_duration'].days
        message += f"- {title}: Количество взятых в аренду: {count}, Средний срок аренды: {avg_duration} дней\n"
    
    emails = list(User.objects.values_list('email', flat=True))
    send_mail('Статистика аренды книг за сутки', message, "red_promo@example.com", emails)