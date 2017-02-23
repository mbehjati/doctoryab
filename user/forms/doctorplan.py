from django import forms


class DoctorFreeTimes(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    visit_duration = forms.Select()

    def is_data_valid(self):
        if self.start_date == '' or self.end_date == '' or self.start_time == '' or self.end_time == '':
            return False
        if self.start_date > self.end_date:
            return False
        if 'pm' in self.start_time and 'am' in self.end_time:
            return False
        if 'am' in self.start_time and 'pm' in self.end_time:
            return True
        if '12:' in self.start_time and '12:' not in self.end_time:
            return True
        if self.start_time >= self.end_time:
            return False
        return True

        # def __init__(self , start_date , end_date , start_time , end_time , duration):
        #     self.start_date = start_date
        #     self.end_date = end_date
        #     self.start_time = start_time
        #     self.end_time = end_time
        #     self.visit_duration = duration
