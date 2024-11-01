from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename, [1] returns extension
    valid_extensions = ['.jpeg', '.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Please upload .jpeg, .jpg, or .png format files.')

def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5 MB limit
        raise ValidationError("File size should not exceed 5 MB")

class Complain(models.Model):
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)
    issue_description = models.TextField()
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES)
    confidence_score = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addon = models.CharField(max_length=500, default='')
    video = models.FileField(upload_to='complain_videos/', blank=True, null=True)

    # New Fields
    incident_datetime = models.DateTimeField(default=None)  # Incident Date and Time

    


    # National ID Validation
    national_id = models.FileField(
        upload_to='national_ids/',
        validators=[validate_image_extension, validate_file_size],
       
    )

    # Financial Fraud Fields (Optional)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    transaction_id = models.CharField(max_length=12, blank=True, null=True)
    transaction_date = models.DateField(blank=True, null=True)
    fraud_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Relevant evidences (File size should not exceed 10MB)
    evidence = models.FileField(
        upload_to='relevant_evidences/',
        validators=[validate_file_size],
        blank=True,
        null=True
    )

    # Optional/Desirable Information
    suspect_website_urls = models.TextField(blank=True, null=True)  # Suspected website URLs
    suspect_mobile_no = models.CharField(max_length=15, blank=True, null=True)
    suspect_email = models.EmailField(blank=True, null=True)
    suspect_bank_account_no = models.CharField(max_length=20, blank=True, null=True)
    suspect_address = models.TextField(blank=True, null=True)
    suspect_photo = models.FileField(
        upload_to='suspect_photos/',
        validators=[validate_image_extension, validate_file_size],
        blank=True,
        null=True
    )
    suspect_other_document = models.FileField(
        upload_to='suspect_documents/',
        validators=[validate_file_size],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Complain ({self.category} - {self.priority})"
