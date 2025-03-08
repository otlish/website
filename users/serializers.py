from rest_framework import serializers
 
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
   
    
    
    password=serializers.CharField(min_length=8,write_only=True)
    confirm_password=serializers.CharField(write_only=True)

    class Meta:
        model=CustomUser
        fields = ['first_name','last_name', 'username','email', 'password', 'confirm_password']

    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        # Check if password and confirm_password match
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before saving
        user = CustomUser.objects.create_user(**validated_data)  # Create user
        return user
