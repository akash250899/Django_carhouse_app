from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from contacts.models import Contact
from cars.models import Car
from django.shortcuts import render


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username = username, password = password)
        # if the user is in the database, then user object will not be none
        # else it will be none

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in !!!")
            return redirect('dashboard')
        messages.error(request, "Invalid Credentials !!!")
        # return redirect('login')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                # Display an error message that this username is already present in our database
                messages.error(request, "Username already exists !!!")
                return redirect('register')
            
            if User.objects.filter(email=email).exists():
                # Display an error message that this email is already present in our database
                messages.error(request, "Email already exists !!!")
                return redirect('register')
            
            user = User.objects.create_user(first_name = firstname,
                                            last_name = lastname,
                                            username = username,
                                            email = email,
                                            password = password)
            user.save()
            # display a success message that the user is created in our database
            messages.success(request, "You are successfully registered !!!")
            return redirect('login')
        else:
            messages.error(request, "Passwords didn't match !!!")
            return redirect('register')

    return render(request, 'accounts/register.html')

def dashboard(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        contacts = Contact.objects.filter(user_id = user_id)
        prices = []
        for contact in contacts:
            car_id = contact.car_id
            car = Car.objects.filter(id = car_id).first()
            print(car)
            price = car.price
            prices.append(price)
        
        data = {
            'contacts': zip(contacts, prices)
        }
        
        return render(request, 'accounts/dashboard.html', context=data)
    messages.error(request, "Sorry you are not allowed to access this page !!!")
    return redirect('login')

def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out successfully !!!")
    return redirect('login')