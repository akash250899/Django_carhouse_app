from django.core import paginator
from django.shortcuts import render, get_object_or_404
from .models import Car
from django.core.paginator import Paginator
from django.db.models import Max, Min

# Create your views here.
def cars(request):
    cars = Car.objects.order_by('created_date')
    paginator = Paginator(cars, 4)
    page = request.GET.get('page')
    page_cars = paginator.get_page(page)

    # Fetching information from the database
    model_search = Car.objects.values_list('model', flat=True).distinct()
    state_search = Car.objects.values_list('state', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    transmission_search = Car.objects.values_list('transmission', flat=True).distinct()
    min_price = Car.objects.all().aggregate(Min('price'))['price__min']
    max_price = Car.objects.all().aggregate(Max('price'))['price__max']

    # Passing information to the cars HTML template
    data = {
        # 'cars': cars,
        'cars': page_cars,
        'model_search': model_search,
        'state_search': state_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
        'transmission_search': transmission_search,
        
        # 'min_price_1': min_price,
        'max_price': max_price,
    }
    return render(request, 'cars/cars.html', context=data)

def car_detail(request, pk):
    car = get_object_or_404(Car, id=pk)
    data = {
        'car': car,
    }
    return render(request, "cars/car-details.html", context=data)