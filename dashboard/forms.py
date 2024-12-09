from django import forms

class PeriodForm(forms.Form):
    PERIOD_CHOICES = [
        ('last_week', 'Last Week'),
        ('last_month', 'Last Month'),
        ('last_year', 'Last Year'),
        ('ytd', 'Year to Date'),
        ('mtd', 'Month to Date'),
        ('custom', 'Custom Date Range'),
    ]
    period = forms.ChoiceField(choices=PERIOD_CHOICES, required=True)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))