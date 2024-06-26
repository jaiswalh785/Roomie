from rest_framework import serializers
from .models import User

class InsertUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'user_type', 'phone_number']
