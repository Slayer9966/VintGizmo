from celery import shared_task
from django.utils import timezone
from .models.return_refund import ReturnRefund

@shared_task
def process_pending_refunds():
    pending_returns = ReturnRefund.objects.filter(return_status='Approved', refund_status__isnull=True)
    for return_request in pending_returns:
        return_request.refund_amount = return_request.order.total_amount  # Example logic
        return_request.refund_status = 'Completed'
        return_request.refund_processed_at = timezone.now()
        return_request.save()