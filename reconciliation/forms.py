from django import forms
from django.core.validators import FileExtensionValidator


class CSVUploadForm(forms.Form):
    """
    CSV file upload form
    """

    first_file = forms.FileField(validators=[FileExtensionValidator(["csv"])])
    second_file = forms.FileField(validators=[FileExtensionValidator(["csv"])])
