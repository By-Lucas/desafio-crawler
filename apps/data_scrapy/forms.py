from django import forms


class ScheduleForm(forms.Form):
    update_time = forms.TimeField()