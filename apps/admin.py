from django.contrib import admin
from apps.apartment.models import *
from apps.users.models import *

admin.site.register(Housing)
admin.site.register(Address)
admin.site.register(User)



