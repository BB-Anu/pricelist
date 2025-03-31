from django.db import models
from django.contrib import admin
# Create your models here.
class PharmaProduct(models.Model):
    company = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    composition = models.TextField()
    packing = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product

# Admin Configuration
class PharmaProductAdmin(admin.ModelAdmin):
    list_display = ('company', 'product', 'composition', 'packing', 'mrp', 'rate')
    search_fields = ('company', 'product')
    ordering = ('company', 'product')
