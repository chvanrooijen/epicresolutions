from django.shortcuts import render
from .models import PDFDownloadLog
from .forms import PeriodForm
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, datetime

def dashboard_view(request):
    form = PeriodForm(request.GET or None)
    current_period = request.GET.get('period', 'last_month week')
    start_date = None
    end_date = None

    if current_period == 'last_week':
        start_date = timezone.now() - timedelta(days=7)
    elif current_period == 'last_month':
        start_date = timezone.now() - timedelta(days=30)
    elif current_period == 'last_year':
        start_date = timezone.now() - timedelta(days=365)
    elif current_period == 'ytd':
        start_date = datetime(timezone.now().year, 1, 1)
    elif current_period == 'mtd':
        start_date = datetime(timezone.now().year, timezone.now().month, 1)
    elif current_period == 'custom':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        start_date = timezone.now() - timedelta(days=7)  # Default to last week

    logs = PDFDownloadLog.objects.filter(timestamp__date__gte=start_date)
    if end_date:
        logs = logs.filter(timestamp__date__lte=end_date)

    downloads_by_date = logs.extra({'date': "date(timestamp)"}).values('date').annotate(count=Count('id'))
    roles_count = logs.values('roles__name').annotate(count=Count('roles')).order_by('-count')
    resolutions_count = logs.values('resolutions__positive_action').annotate(count=Count('resolutions')).order_by('-count')

    context = {
        'form': form,
        'downloads_by_date': downloads_by_date,
        'roles_count': roles_count,
        'resolutions_count': resolutions_count,
    }
    return render(request, 'dashboard/dashboard.html', context)