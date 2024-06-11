from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('professional', 'Working Professional'),
        ('other', 'Other'),
    )
    user_uuid = models.CharField(max_length=45)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # phone_number = models.CharField(max_length=15, null=True, blank=True)
    # phone_number = models.CharField(max_length=15, null=True, blank=True)
    def __str__(self):
        return self.username

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('pg', 'PG'),
        ('hostel', 'Hostel'),
        ('apartment', 'Apartment'),
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    description = models.TextField()
    owner = models.ForeignKey(User, limit_choices_to={'user_type': 'owner'}, on_delete=models.CASCADE, related_name='properties')

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.room_type} Room in {self.property.name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room}"
    
class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_amenities')
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name='property_amenities')
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.amenity.name} at {self.property.name}"

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.property.name}"

from django.contrib import admin
from .models import User, Property, Room, Booking, Amenity, PropertyAmenity, Review

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_type', 'city', 'owner')
    list_filter = ('property_type', 'city')
    search_fields = ('name', 'address', 'city', 'state')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.user_type == 'owner':
            return queryset.filter(owner=request.user)
        return queryset

    def save_model(self, request, obj, form, change):
        if request.user.user_type == 'owner' and not change:
            obj.owner = request.user
        obj.save()

admin.site.register(User)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Amenity)
admin.site.register(PropertyAmenity)
admin.site.register(Review)
