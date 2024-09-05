from django.contrib import admin
from apps.apartment.apartment_models import *
from apps.users.users_models import User

admin.site.register(Housing)
admin.site.register(Address)
admin.site.register(User)


