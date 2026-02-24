from django.db import models
import uuid
from cloudinary.models import CloudinaryField

# Create your models here.

# models.py
class Review(models.Model):
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}⭐"


class ServiceRequest(models.Model):
    SERVICE_CHOICES = [
        ('web', 'Web'),
        ('mobile', 'Mobile'),
        ('design', 'Design'),
        ('office', 'Office'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    description = models.TextField()
    is_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"


class Quote(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    is_approved = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Devis - {self.request.email}"

        
class EmailLog(models.Model):
    quote = models.ForeignKey("Quote", on_delete=models.CASCADE, related_name="emails")
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=False)  # renvoi manuel

    def __str__(self):
        return f"{self.recipient} | {self.sent_at:%d/%m/%Y %H:%M}"
    

class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    browser = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    device = models.CharField(max_length=50)
    user_agent = models.TextField()
    page = models.CharField(max_length=255)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.browser}"
    

class Project(models.Model):

    STATUS_CHOICES = (
        ('realise', 'Réalisé'),
        ('encours', 'En cours'),
        ('futur', 'Futur'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    #image = models.ImageField(upload_to='projects/', blank=True, null=True)
    image = CloudinaryField('image', folder='projects', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    technologies = models.CharField(
        max_length=255,
        blank=True,
        help_text="Ex: Django, Python, Bootstrap"
    )
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class ProjectLike(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="likes_records"
    )
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "ip_address", "session_key")

    def __str__(self):
        return f"Like on project {self.project_id}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    

class Certification(models.Model):

    STATUS_CHOICES = (
        ('obtenue', 'Obtenue'),
        ('encours', 'En cours'),
        ('future', 'Prévue'),
    )

    title = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    #logo = models.ImageField(upload_to='certifications/logos/', blank=True, null=True)
    logo = CloudinaryField('logo', folder='certifications/logos', blank=True, null=True)

    description = models.TextField()
    technologies = models.CharField(max_length=255, blank=True)

    issued_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)

    credential_id = models.CharField(max_length=255, blank=True)
    credential_url = models.URLField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    level = models.CharField(max_length=50, blank=True)

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question
    

class Suggestion(models.Model):
    name_sug = models.CharField(max_length=100)
    email_sug = models.EmailField(blank=True)
    message_sug = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_sug

class SuggestionLike(models.Model):
    suggestion = models.ForeignKey(
        Suggestion,
        on_delete=models.CASCADE,
        related_name="likes_records"
    )
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("suggestion", "ip_address", "session_key")

    def __str__(self):
        return f"Like on {self.suggestion_id}"