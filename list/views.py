from django.shortcuts import render
import pandas as pd
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from decimal import Decimal, InvalidOperation
from list.models import PharmaProduct

# Create your views here.
def import_excel(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        df = pd.read_excel(file_path)  # Specify separator

        # Replace NaN values with default values
        df.fillna({'COMPANY': '', 'PRODUCT': '', 'COMPOSITION': '', 'PACKING': '', 'MRP': 0, 'RATE': 0}, inplace=True)



        for _, row in df.iterrows():
            try:
                # Ensure string conversion and strip spaces
                mrp_value = str(row['MRP']).strip()
                rate_value = str(row['RATE']).strip()

                # Remove any non-numeric characters except for decimal points
                mrp_value = ''.join(c for c in mrp_value if c.isdigit() or c == '.')
                rate_value = ''.join(c for c in rate_value if c.isdigit() or c == '.')

                # Convert to Decimal, fallback to 0.00 if invalid
                mrp_value = Decimal(mrp_value) if mrp_value else Decimal('0.00')
                rate_value = Decimal(rate_value) if rate_value else Decimal('0.00')

            except (InvalidOperation, ValueError):
                mrp_value = Decimal('0.00')  # Default value if conversion fails
                rate_value = Decimal('0.00')

            PharmaProduct.objects.create(
                company=row['COMPANY'],
                product=row['PRODUCT'],
                composition=row['COMPOSITION'],
                packing=row['PACKING'],
                mrp=mrp_value,
                rate=rate_value
            )


        return JsonResponse({'message': 'File imported successfully'})

    return render(request, 'import_excel.html')

from rapidfuzz import fuzz
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import PharmaProduct

def list_products_view(request):
    company = request.GET.get('company', '')
    composition = request.GET.get('composition', '')
    page = request.GET.get('page', 1)
    per_page = 30  

    products = PharmaProduct.objects.all()

    if company:
        products = products.filter(company__icontains=company)

    if composition:
        similar_products = []
        for product in products:
            similarity_score = fuzz.partial_ratio(composition.lower(), product.composition.lower())
            if similarity_score > 90: 
                similar_products.append(product)

        products = similar_products

    # Apply pagination
    paginator = Paginator(products, per_page)
    paginated_products = paginator.get_page(page)

    context = {
        'products': paginated_products,
        'total_pages': paginator.num_pages,
        'current_page': int(page),
        'selected_company': company,
        'selected_composition': composition,
    }
    return render(request, 'list_products.html', context)
