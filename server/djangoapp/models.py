# Imports
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    """Model representing a car make (brand)."""
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name  # Return the name as the string representation


class CarModel(models.Model):
    """Model representing a specific car model."""
    car_make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE, related_name="models"
    )  # Many-to-One relationship
    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as required
    ]

    type = models.CharField(
        max_length=10, choices=CAR_TYPES, default='SUV'
    )
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
