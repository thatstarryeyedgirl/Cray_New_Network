from rest_framework import serializers # Imports Django REST Framework’s serializer classes, which help convert data between python objects and JSON
from django.contrib.auth import authenticate, get_user_model # Imports authenticate (for login validation) and get_user_model (to fetch the active custom user model)
from django.core.mail import send_mail
from .models import ChiefEditor
from django.conf import settings


ChiefEditor = get_user_model() # Fetches the active user model, which is ChiefEditor in this case


class ChiefEditorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required  = True) # the password field is required but write-only — meaning it can be sent by the user but never returned in API responses
    
    class Meta:
        model = ChiefEditor
        fields = ['first_name','last_name' ,'email', 'profile_picture', 'password']
        
        
    def validate(self, attrs):
        required_fields = ['first_name', 'last_name', 'email', 'password', 'profile_picture']

        # Check missing fields
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({field: f"{field} is required."})

        # Password validation
        password = attrs.get('password')
        if len(password) < 12:
            raise serializers.ValidationError({"password": "Password must be at least 12 characters long."})
        
        
        return attrs
        
    # creates a new ChiefEditor user using the model’s create_user() method, which automatically hashes the password before saving
    def create(self, validated_data):
        user = ChiefEditor.objects.create_user(
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            password=validated_data['password'],
            profile_picture=validated_data['profile_picture']
        )
        
        # Send welcome email
        try:
            send_mail(
                subject="Welcome to Cray New Network!",
                message=f"Hi {user.first_name},\n\nWelcome to Cray New Network! Your account has been created successfully.\n\nBest regards,\nCNN Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception:
            pass
            
        return user
    
    
class ChiefEditorLoginSerializer(serializers.Serializer): # a plain serializer (not model-based) for validating login credentials defines the two fields users must provide to log in
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data): # extracts email and password from user input
        email = data.get("email")
        password = data.get("password")

        # authenticates the user using Django’s authentication system; raises errors for missing or invalid credentials, then attaches the user object to the validated data
        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password) # it checks if the given email and password match a valid user in the database, If the credentials are correct → it returns a user object
            if not user:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Both email and password are required")

        data["user"] = user # data here represents the clean, validated data that passed through the serializer then adding user into it means that after validation, the serializer will contain
        return data # the serializer returns the cleaned and validated data (including the user object)
    
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField() # collects the email address of the user who wants to reset their password

    # checks that the provided email actually exists in the database; raises an error if it doesn’t
    def validate_email(self, value):
        if not ChiefEditor.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    # collects two password fields (new and confirm) for resetting a user’s password
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        # checks that the new password and confirm password fields match; raises an error if they don’t
        if data.get("new_password") != data.get("confirm_password"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    

#