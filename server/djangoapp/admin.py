from django.contrib import admin
from .models import CarMake, CarModel  # Import your models


# CarModelInline class - Allows editing CarModel within CarMake
class CarModelInline(admin.TabularInline):  
    """Allows inline editing of CarModel inside CarMake."""
    model = CarModel
    extra = 1  # Show 1 empty row for adding new CarModels within CarMake


# CarModelAdmin class - Custom admin options for CarModel
class CarModelAdmin(admin.ModelAdmin):
    """Admin configuration for CarModel."""
    list_display = ('name', 'car_make', 'type', 'year')
    list_filter = ('car_make', 'type', 'year')
    search_fields = ('name', 'car_make__name')


# CarMakeAdmin class - Registers CarMake and includes CarModel inline
class CarMakeAdmin(admin.ModelAdmin):
    """Admin configuration for CarMake with inline CarModel."""
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [CarModelInline]  # Allows adding CarModels inside CarMake


# Register models with Django admin
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
