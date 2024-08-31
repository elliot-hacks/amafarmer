from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from .models import *
from .forms import *
import calendar
from .utils import Calendar


# Create your views here.
def index(request):
    return HttpResponse("Hello farmers")


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('home:cal/calendar'))
    return render(request, 'cal/event.html', {'form': form})


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Use the 'month' GET parameter to get the date; default to current month
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our Calendar class with the selected year and month
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method to get the calendar as an HTML table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        # Add the previous and next month links to the context
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        return context


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    return f'month={prev_month.year}-{prev_month.month:02d}'

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    return f'month={next_month.year}-{next_month.month:02d}'


def get_date(req_day):
    if req_day:
        year, month = map(int, req_day.split('-'))
        return datetime(year, month, 1)
    return datetime.today().replace(day=1)

