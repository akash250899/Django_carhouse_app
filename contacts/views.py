from django.shortcuts import redirect, render
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def inquiry(request):
    if request.method == "POST":
        car_id = request.POST['car_id']
        car_title = request.POST['car_title']
        user_id = request.POST['user_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        customer_need = request.POST['customer_need']
        city = request.POST['city']
        state = request.POST['state']
        message = request.POST['message']
        email = request.POST['email']
        phone = request.POST['phone']

        if request.user.is_authenticated:
            has_contacted = Contact.objects.filter(car_id=car_id, user_id=user_id)
            if has_contacted:
                messages.error(request, "You have already contacted us about this car, please wait for some time")
                return redirect('/cars/car/' + car_id)

        contact = Contact(car_id=car_id, car_title=car_title,
                          user_id = user_id, first_name=first_name,
                          last_name = last_name, customer_need=customer_need,
                          city=city, state=state, message=message,
                          email=email, phone=phone)

        admin_info = User.objects.get(is_superuser = True)
        admin_email = admin_info.email

        send_mail(
            'New Car enquiry: ' + car_title,
            'You have an new enquiry for the car ' + car_title + '. Login for more details',
            email,
            [admin_email],
            fail_silently=False,
        )
        contact.save()
        messages.success(request, "Your request has been submitted !! we will get back to you soon")
        return redirect('/cars/car/' + car_id)
    else:
        return redirect('home')