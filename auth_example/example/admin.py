from example.models import ExampleUserProfile
from django.contrib import admin


class ExampleUserProfileAdmin(admin.ModelAdmin):
    pass
## END ExampleUserProfileAdmin
admin.site.register(ExampleUserProfile, ExampleUserProfileAdmin)