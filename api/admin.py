from django.contrib import admin

from .models.auth import Auth
from .models.parking_slot import ParkingSlot
from .models.password_recovery import PasswordRecovery
from .models.payment import Payment
from .models.reservation import Reservation
from .models.user import User

# Register your models here.
admin.site.register(Auth)
admin.site.register(ParkingSlot)
admin.site.register(PasswordRecovery)
admin.site.register(Payment)
admin.site.register(Reservation)
admin.site.register(User)