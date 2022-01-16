from django.shortcuts import render
import random
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from car_rental_APP.models import Car, District, Orders, User
from car_rental_APP.forms import (
    LoginForm,
    CarAddForm,
    CustomerRegistrationForm,
    CarDealerRegistrationForm,
    CarSearchForm,
)
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()


# Create your views here.


class IndexView(View):
    """Main site view"""
    def get(self, request):
        all_cars = list(Car.objects.all())
        random.shuffle(all_cars)
        return render(request, "index.html", {"car_1": all_cars[0],
                                              "car_2": all_cars[1],
                                              "car_3": all_cars[2]},)


class CarListView(View):
    """List of cars view"""
    def get(self, request):

        list_of_cars = Car.objects.all()

        paginator = Paginator(list_of_cars, 20)
        page = request.GET.get("page")
        cars = paginator.get_page(page)
        list_of_cars = [
            i for i in range(1, cars.paginator.num_pages + 1)]
        ctx = {"cars": cars, "list_of_cars": list_of_cars}
        return render(request, "car_list_view.html", ctx)


class CarDetailedView(View):
    """Detailed view one of chosen car"""
    def get(selfself, request, car_id):
        car = Car.objects.get(id=car_id)
        return render(request, "car_detailed_view.html", {"car": car})


class RegisterView(View):
    """New user registration - main page."""
    """It is possible to choose type of user to register """
    def get(self, request):
        return render(request, "register.html")


class CarDealerRegistrationView(View):
    """Car dealer registration view"""
    def get(self, request):
        form = CarDealerRegistrationForm()
        return render(
            request, "car_dealer_registration_form.html", {"form": form})

    def post(self, request):
        form = CarDealerRegistrationForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            email = form.cleaned_data["email"]
            User.objects.create_user(
                username=login,
                email=email,
                password=password,
                first_name=name,
                last_name=surname,
                is_car_dealer=True)
            return redirect("/login/")
        else:
            return render(request, "car_dealer_registration_form.html", {"form": form})


class CustomerRegistrationView(View):
    """Car dealer registration view"""
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(
            request, "customer_registration_form.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            email = form.cleaned_data["email"]
            User.objects.create_user(
                username=login,
                email=email,
                password=password,
                first_name=name,
                last_name=surname,
                is_customer=True)
            return redirect("/login/")
        else:
            return render(
                request, "customer_registration_form.html", {"form": form})


class LoginView(View):
    """User login page. Redirection to locked customer or car dealer portals"""
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                login=form.cleaned_data["login"],
                password=form.cleaned_data["password"],)

            if user is not None:
                if user.is_car_dealer == True:
                    login(request, user)
                    return redirect('/car_dealer_portal')
                elif user.is_customer == True:
                    login(request, user)
                    return redirect('/customer_portal')
                else:
                    return redirect('/login')
        return render(request, "login.html", {'form': form})


    #if user is not None:
    # if user.is_customer == True:
    #     return redirect('/customer_portal')
    # elif user.is_car_dealer == True:
    #     return redirect('/car_dealer_portal')


class LogoutView(View):
    """Logout view. Back to home page"""
    def get(self, request):
        logout(request)
        return redirect("/")


# === CAR_DEALER_PORTAL ===#


class CarDealerPortalView(LoginRequiredMixin, View):
    """Car dealer portal's page- main view. Possibility to go to detailed pages"""
    """Login required"""
    login_url = "/login/"

    def get(self, request):
        return render(request, "car_dealer_portal_view.html")


class CarAddView(LoginRequiredMixin, View):
    """New car adding form view"""
    login_url = "/login/"

    def get(self, request):
        form = CarAddForm()
        return render(request, "add_car.html", {"form": form})

    def post(self, request):
        form = CarAddForm(request.POST)
        if form.is_valid():
            car_name = form.cleaned_data["car_name"]
            color = form.cleaned_data["color"]
            dealer = form.cleaned_data["dealer"]
            district = form.cleaned_data["district"]
            capacity = form.cleaned_data["capacity"]
            is_available = form.cleaned_data["is_available"]
            engine = form.cleaned_data["engine"]
            ac = form.cleaned_data["ac"]
            description = form.cleaned_data["description"]
            car = Car.objects.create(  # tworzymy nowy samochód
                car_name=car_name,
                color=color,
                dealer=dealer,
                district=district,
                capacity=capacity,
                is_available=is_available,
                engine=engine,
                ac=ac,
                description=description,
            )
            return redirect(
                f"/car_detailed_view/{car.id}/"
            )  # przekierowanie linku
        else:
            return render(
                request, "/car_dealer_portal/add_car/", {"form": form}
            )


class CarsView(LoginRequiredMixin, View):
    """Customer portal's page- main view. Possibility to go to detailed pages """
    """LLogin required"""
    login_url = "/login/"

    def get(self, request):
        car_list = []
        cars = Car.objects.filter()
        for c in cars:
            car_list.append(c)
        return render(request, "car_list.html", {"car_list": car_list})


class CarOrderView(LoginRequiredMixin, View):
    """List of ordered cars"""
    login_url = "/login/"

    def get(self, request):
        orders = Orders.objects.filter()
        order_list = []
        for ord in orders:
            if ord.is_complete == False:
                order_list.append(ord)
        return render(request, "order_list.html", {"order_list": order_list})


# === CUSTOMER_PORTAL ===#

class CustomerPortalView(LoginRequiredMixin, View):
    """Customer portal's page- main view. Possibility to go to detailed pages"""
    """Login required"""
    login_url = "/login/"

    def get(self, request):
        return render(request, "customer_portal_view.html")


class CarSearchView(LoginRequiredMixin, View):
    """Searching by district pagr"""
    login_url = "/login/"

    def get(self, request):
        form = CarSearchForm()
        return render(request, "search_car.html", {"form": form})

    def post(self, request):
        form = CarSearchForm(request.POST)
        if form.is_valid():
            districts = District.objects.filter(
                district_name__icontains=form.cleaned_data["district_name"]
            )
            return render(
                request,
                "search_car.html",
                {"form": form, "districts": districts},
            )


# class CarSearchResultsView(LoginRequiredMixin, View):
#
#     login_url = '/login/'
#
#     def get(self, request):
#         form = CarSearchResultsForm()
#         return render(request, 'search_results.html', {'form': form})pip
#
#     def post(self, request):
#         form = CarSearchResultsForm(request.POST)
#         if form.is_valid():
#             district_name = request.POST['district_name']
#             district_name = district_name.lower()
#             cars_list = []
#             district = District.objects.filter(district_name=district_name)
#             for d in district:
#                 cars = Car.objects.filter(district=d)
#                 for car_av in cars:
#                     if car_av.is_available == True:
#                         car_dictionary = {'name': car_av.car_name, 'color': car_av.color, 'id': car_av.id,
#                                         'pincode': car_av.district.pincode, 'capacity': car_av.capacity,
#                                         'engine': car_av.engine, 'description': car_av.description,
#                                         'dealer': car_av.dealer}
#                         cars_list.append(car_dictionary)
#                         request.session['cars_list'] = cars_list
#             return render(request, 'search_results.html', {'car_dictionary': car_dictionary})
#         else:
#             return render(request, 'search_results.html')

