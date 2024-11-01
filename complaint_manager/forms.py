from django import forms
from .models import Complain

class ComplainForm(forms.ModelForm):
    video = forms.FileField(required=False)  # Make video field optional
    addon = forms.CharField(widget=forms.Textarea, required=False)  # Use Textarea for addon

    class Meta:
        model = Complain
        fields = [
         
            'issue_description',
           
            'incident_datetime',
            
            'national_id',
            'bank_name',
            'transaction_id',
            'transaction_date',
            'fraud_amount',
            'evidence',
            'suspect_website_urls',
            'suspect_mobile_no',
            'suspect_email',
            'suspect_bank_account_no',
            'suspect_address',
            'suspect_photo',
            'suspect_other_document',
            'video',
            'addon'
        ]

        widgets =  {
            'issue_description': forms.Textarea(attrs={'class': 'form-control'}),
            'incident_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fraud_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'suspect_website_urls': forms.Textarea(attrs={'class': 'form-control'}),
            'suspect_mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'suspect_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'suspect_bank_account_no': forms.TextInput(attrs={'class': 'form-control'}),
            'suspect_address': forms.Textarea(attrs={'class': 'form-control'}),
            'suspect_photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'suspect_other_document': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

   