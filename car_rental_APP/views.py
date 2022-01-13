from django.shortcuts import render
import random
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import auth
from car_rental_APP.models import Car, CarDealer, District, Customer
from car_rental_APP.forms import LoginForm, CarAddForm, CustomerRegistrationForm, CarDealerRegistrationForm
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()
from django.contrib.auth.decorators import login_required


# Create your views here.

class IndexView(View):
    def get(self, request):
        #ctx = {"actual_date": datetime.now()}
        all_cars = list(Car.objects.all())
        random.shuffle(all_cars)
        return render(request, "index.html", {'car_1': all_cars[0],
                                              'car_2': all_cars[1],
                                              'car_3': all_cars[2]})

class CarListView(View):
    def get(self, request):

        list_of_cars = Car.objects.all()

        paginator = Paginator(list_of_cars, 20)  # ustawienie ile elementów ma pojawiać się na stronie
        page = request.GET.get('page')
        cars = paginator.get_page(page)
        list_of_cars = [i for i in range(1, cars.paginator.num_pages + 1)]  # lista do interowania w for do środkowej części paginatora

        ctx = {'cars': cars, 'list_of_cars': list_of_cars}
        return render(request, 'car_list_view.html', ctx)

class CarDetailedView(View):
    def get(selfself, request, car_id):
        car = Car.objects.get(id=car_id)
        return render(request, 'car_detailed_view.html', {'car': car})


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')


class CarDealerRegistrationView(View):
    def get(self, request):
        form = CarDealerRegistrationForm()
        return render(request, 'car_dealer_registration_form.html', {'form': form})

    def post(self, request):
        form = CarDealerRegistrationForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            User.objects.create_user(username=login, email=email, password=password, first_name=name, last_name=surname)
            return redirect('/login/') #HttpResponse('Stworzono użytkownika - Dealer samochodów')
        else:
            return render(request, 'car_dealer_registration_form.html', {'form': form})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'customer_registration_form.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            User.objects.create_user(username=login, email=email, password=password, first_name=name, last_name=surname)
            return redirect('/login/') #HttpResponse('Stworzono użytkownika - klient')
        else:
            return render(request, 'customer_registration_form.html', {'form': form})


class LooginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        form.is_valid()
        user = authenticate(username=form.cleaned_data['login'],
                            password=form.cleaned_data['password'])
        if user:  # user jest w bazie
            login(request, user)
        # if user.is_customer = True
        #     return redirect('customer_portal/')
        # elif user.is_car_dealer = True
        #     return redirect('car_dealer_portal/')
            return redirect('/')
        else:  # nie ma user-a
            return render(request, 'login.html', {'form': form, 'message': 'Błędny login lub hasło'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class CarDealerPortalView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        return render(request, 'car_dealer_portal_view.html')

class CustomerPortalView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        return render(request, 'customer_portal_view.html')

#
# def register(request):
#     return render(request, '../templates/register.html')


class CarAddView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        form = CarAddForm()
        return render(request, 'add_car.html', {'form': form})

    def post(self, request):
        form = CarAddForm(request.POST)
        if form.is_valid():
            car_name = form.cleaned_data['car_name']
            color = form.cleaned_data['color']
            dealer = form.cleaned_data['dealer']
            district = form.cleaned_data['district']
            capacity = form.cleaned_data['capacity']
            is_available = form.cleaned_data['is_available']
            engine = form.cleaned_data['engine']
            ac = form.cleaned_data['ac']
            description = form.cleaned_data['description']
            car = Car.objects.create( #tworzymy nowy samochód
                car_name=car_name,
                color=color,
                dealer=dealer,
                district=district,
                capacity=capacity,
                is_available=is_available,
                engine=engine,
                ac=ac,
                description=description
            )
            return redirect(f'/car_detailed_view/{car.id}/') #przekierowanie linku
        else:
            return render(request, '/car_dealer_portal/add_car/', {'form': form})






#
# class PasswordResetView(PermissionRequiredMixin, View):
#     permission_required = 'auth.change_user'
#
#     def get(self, request, user_id):
#         form = PasswordResetForm()
#         return render(request, '/reset.html', {'form': form})
#
#     def post(self, request, user_id):
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             user = User.objects.get(id=user_id)
#             user.set_password(form.cleaned_data['password1'])
#             user.save()
#             return redirect('/')
#         else:
#             return render(request, '/reset.html', {'form': form})