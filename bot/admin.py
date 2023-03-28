from django.contrib import admin
from .models import UserInformation,Ids,Log,Department
# Register your models here.


admin.site.register(UserInformation)
admin.site.register(Ids)
admin.site.register(Log)
admin.site.register(Department)