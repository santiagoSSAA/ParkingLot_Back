"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.urls import path

from .views.auth import AuthApi
from .views.auth import RefreshTokenApi
from .views.user.general import UserApi
from .views.user.general import SpecificUserApi
from .views.reservation import ReservationApi
from .views.reservation import SpecificReservationApi
from .views.parking_slot import ParkingSlotApi
from .views.parking_slot import SpecificParkingSlotApi
from .views.password_recovery import PasswordRecoveryApi
from .views.password_recovery import SpecificPasswordRecoveryApi
from .views.payment import PaymentApi

urlpatterns = [
    path("auth", AuthApi.as_view()),
    path('refresh_token/<str:refresh>', RefreshTokenApi.as_view()),
    path('user', UserApi.as_view()),
    path('user/<int:id>', SpecificUserApi.as_view()),
    path('reservation', ReservationApi.as_view()),
    path('reservation/<int:id>', SpecificReservationApi.as_view()),
    path('parking_slot', ParkingSlotApi.as_view()),
    path('parking_slot/<int:id>', SpecificParkingSlotApi().as_view()),
    path('password_recovery', PasswordRecoveryApi.as_view()),
    path('password_recovery/<str:token>', SpecificPasswordRecoveryApi.as_view()),
    path('payment', PaymentApi.as_view()),
]