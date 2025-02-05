from django.contrib import admin
from .models import CarMake, CarModel  # Import your models

# CarModelInline class - Allows editing CarModel within CarMake
class CarModelInline(admin.TabularInline):  # You can use `admin.StackedInline` for a different layout
    model = CarModel
    extra = 1  # Show 1 empty row for adding new CarModels within CarMake

# CarModelAdmin class - Custom admin options for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')  # Fields shown in the admin list view
    list_filter = ('car_make', 'type', 'year')  # Filters on the right panel
    search_fields = ('name', 'car_make__name')  # Enables searching by model and make

# CarMakeAdmin class - Registers CarMake and includes CarModel inline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Fields shown for CarMake in the admin
    search_fields = ('name',)  # Enables searching for CarMakes
    inlines = [CarModelInline]  # Allows adding CarModels inside CarMake

# Register models with Django admin
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
