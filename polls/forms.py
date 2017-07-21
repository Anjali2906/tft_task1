from django import forms
from .models import CSVFile, SubFile
# from nested_forms import ComplexModelForm

class CSVFileForm(forms.ModelForm):
	class Meta:
		model = CSVFile
		fields = ('name_of',)

class SubFileForm():
    class Meta:
        model = SubFile
        fields =('pid', 'my_file', 'description')

