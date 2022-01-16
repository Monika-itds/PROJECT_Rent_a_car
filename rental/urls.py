"""rental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from django.conf.urls.static import static
# from django.conf import settings

from car_rental_APP.views import (
    IndexView,
    CarListView,
    CarDetailedView,
    CarAddView,
    LoginView,
    LogoutView,
    RegisterView,
    CustomerRegistrationView,
    CarDealerRegistrationView,
    CarDealerPortalView,
    CustomerPortalView,
    CarsView,
    CarOrderView,
    CarSearchView,
    #CarSearchResultsView,
)


app_name = "car_rental_APP"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view()),
    path("car_list/", CarListView.as_view(), name="CarListView"),
    path("car_detailed_view/<int:car_id>/", CarDetailedView.as_view(), name="CarDetailedView",),
    path("register/", RegisterView.as_view(), name="Register"),
    path("add_car_dealer/", CarDealerRegistrationView.as_view(), name="Register"),
    path("add_customer/", CustomerRegistrationView.as_view(), name="CustomerRegistrationView",),
    path("login/", LoginView.as_view(), name="LoginView"),
    path("logout/", LogoutView.as_view(), name="LogoutView"),
# car_dealer_portal/
    path("car_dealer_portal/", CarDealerPortalView.as_view(), name="CarDealerPortal",),
    path("car_dealer_portal/add_car/", CarAddView.as_view(), name="AddCar"),
    path("car_dealer_portal/cars/", CarsView.as_view(), name="CarList"),  # samochody
# path('car_dealer_portal/car_delete/<int:pk>/', CarDeleteView.as_view(), name='CarDelete')
    path("car_dealer_portal/order_list/", CarOrderView.as_view(), name="CarOrderView",),  # złożone zamówienia
    # customer_portal/
    path("customer_portal/", CustomerPortalView.as_view(), name="CustomerPortal"),
    path( "customer_portal/search_car/", CarSearchView.as_view(), name="SearchCarView"), # wyszukuje po podanym kryterium
    #path("customer_portal/search_results/", CarSearchResultsView.as_view(), name="CarSearchResultsView",),  # wyniki wyszukiwania
    # path('customer_portal/rent_car/', ....View.as_view(), name='...AddView'), #przycisk rent -> przeierowanie do zamówienia
    # path('customer_portal/order/', ....View.as_view(), name='...AddView'),#zamówienie + przeliczenie kaski: cost_per_day = int(car.capacity)*100
    # path('customer_portal/update_order/', ....View.as_view(), name='...AddView'),
    # path('customer_portal/delete_order/', ....View.as_view(), name='...AddView'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#allow to show image in url
