from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rfc = models.CharField(max_length=13, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Colombia', blank=True)
    sector = models.CharField(max_length=120, blank=True)
    employee_count = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'companies_company'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return self.name