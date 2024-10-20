from django import forms
from .models import Notes , Homework , Todo 



class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes 
        fields =["title","descriptions"]

class DeteInput(forms.DateInput):
    input_type = "date"


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ["subject","title","description","due","is_finished"]
        widgets = {
            "due":DeteInput()
        }

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter your search : ")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title","is_finished"]



UNIT_CHOICES = [
    ('meters', 'Meters'),
    ('kilometers', 'Kilometers'),
    ('centimeters', 'Centimeters'),
    ('inches', 'Inches'),
    ('feet', 'Feet')
]

class ConversionForm(forms.Form):
    input_value = forms.FloatField(label='Enter value', required=True)
    from_unit = forms.ChoiceField(choices=UNIT_CHOICES, label='From Unit')
    to_unit = forms.ChoiceField(choices=UNIT_CHOICES, label='To Unit')



    
