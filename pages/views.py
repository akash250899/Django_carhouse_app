from django.shortcuts import render, get_object_or_404
from .models import Team
from cars.models import Car
from django.db.models import Max, Min

# Create your views here.
def home(request):
    teams = Team.objects.all()
    featured_cars = Car.objects.filter(is_featured=True)
    latest_cars = Car.objects.order_by('-created_date')[:3]

    model_search = Car.objects.values_list('model', flat=True).distinct()
    state_search = Car.objects.values_list('state', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    min_price = Car.objects.all().aggregate(Min('price'))['price__min']
    max_price = Car.objects.all().aggregate(Max('price'))['price__max']

    data = {
        'teams': teams,
        'featured_cars': featured_cars,
        'latest_cars': latest_cars,

        'model_search': model_search,
        'state_search': state_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
        
        # 'min_price_1': min_price,
        'max_price_1': max_price,
    }
    return render(request, 'pages/home.html', context=data)

def about(request):
    teams = Team.objects.all()
    data = {
        'teams': teams,
    }
    return render(request, 'pages/about.html', context=data)

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    return render(request, 'pages/contact.html')

def team_detail(request, id):
    member = get_object_or_404(Team, id=id)
    best_employees = Team.objects.filter(is_best=True)
    data = {
        'member': member,
        'best_employees': best_employees,
    }
    return render(request, 'pages/team-detail.html', context=data)

def search(request):
    cars = Car.objects.order_by('created_date')

    model_search = Car.objects.values_list('model', flat=True).distinct()
    state_search = Car.objects.values_list('state', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    transmission_search = Car.objects.values_list('transmission', flat=True).distinct()
    condition_search = Car.objects.values_list('condition', flat=True).distinct()
    max_price = Car.objects.all().aggregate(Max('price'))['price__max']

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cars = cars.filter(description__icontains=keyword)
    
    if 'model' in request.GET:
        model = request.GET['model']
        if model:
            cars = cars.filter(model__iexact=model)
    
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            cars = cars.filter(state__iexact=state)

    if 'year' in request.GET:
        year = request.GET['year']
        if year:
            cars = cars.filter(year__iexact=year)
        
    if 'body_style' in request.GET:
        body_style = request.GET['body_style']
        if body_style:
            cars = cars.filter(body_style__icontains=body_style)
    
    if 'transmission' in request.GET:
        transmission = request.GET['tranmission']
        if transmission:
            cars = cars.filter(tranmission__iexact=transmission)
    
    if 'min_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']
        if max_price != '':
            cars = cars.filter(price__gte=min_price, price__lte=max_price)

    data = {
        'cars': cars,
        'model_search': model_search,
        'state_search': state_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
        'transmission_search': transmission_search,
        'condition_search': condition_search,
        'max_price': max_price,
    }

    return render(request, 'cars/search.html', context=data)