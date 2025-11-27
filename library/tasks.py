from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    today = timezone.now().date()
    overdue_loans=Loan.objects.select_related('member__user', 'book').filter(is_returned=False, due_date__lt=today)

    # TODO maybe use iterator?
    for loan in overdue_loans:
        member_email=loan.member.user.email
        if not member_email:
            logger.warning(f'User "{loan.member.user.username}" does not have an email')
            continue
        try:
            send_mail(
                subject='Overdue Book Reminder',
                message=f'Hello {loan.member.user.username}, The book "{loan.book.title}" is overdue. Please return it as soon as possible.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member_email],
                fail_silently=False,
            )
        except Exception as e:
            logger.exception(f"Failed to send overdue reminder to {member_email}: {str(e)}")