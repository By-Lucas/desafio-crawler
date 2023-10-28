from django import forms


class ScheduleForm(forms.Form):
    update_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'class': 'form-control col-sm-3 mb-3', 'placeholder':'00:00'}))
