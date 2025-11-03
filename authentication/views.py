from django.db import IntegrityError # Handles database errors like duplicate entries
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.authtoken.models import Token #used for API login authentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .serializers import ChiefEditorRegistrationSerializer, ChiefEditorLoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from django.core.mail import send_mail
from .models import ChiefEditor
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # encodes data to base 64 and decodes base 64 data where urlsafe means it avoids special characters that may break URLs
from django.utils.encoding import smart_bytes, force_str # smart_bytes converts data(like base 64) to bytes, force_str converts bytes back to string
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


ChiefEditor = get_user_model() # gets the currently active user model which is ChiefEditor in this case

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs): # Handles POST requests to register a new user where *args and **kwargs allow for additional positional and keyword arguments respectively
        serializer = ChiefEditorRegistrationSerializer(data=request.data, context={"request": request}) # Takes user data from the request and passes it to serializer for validation
        try:
            # Validates the input
            serializer.is_valid(raise_exception=True)

            # Creates user
            user = serializer.save()

        except IntegrityError:
            # Handle case where email already exists
            return Response(
                {"error": "This email is already registered."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"user": ChiefEditorRegistrationSerializer(user).data},
            status=status.HTTP_201_CREATED
        )
        
        
class LoginView(APIView):
    permission_classes = [permissions.AllowAny] # allows anyone to login (no prior authentication needed)

    def post(self, request, *args, **kwargs):
        # validates that email and password are provided
        serializer = ChiefEditorLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        # verifies user credentials
        user = authenticate(request, username=email, password=password)
        if not user: # returns error if authentication fails
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # creates or retrieves an authentication token for the user
        # token, _ = Token.objects.get_or_create(user=user) was removed because we are using JWT now
        return Response(
            { # "token": token.key, 
                "refresh": str(RefreshToken.for_user(user)),
                "access": str(RefreshToken.for_user(user).access_token),
            },status=status.HTTP_200_OK
        )
        

class ForgotPasswordView(APIView):
    permission_classes = [] # no authentication required (anyone can request password reset)

    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = request.data.get("email") # ensures email is provided
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = ChiefEditor.objects.get(email=email) # finds the user with the provided email
        except ChiefEditor.DoesNotExist:
            return Response({"error": "No user found with this email"}, status=status.HTTP_404_NOT_FOUND)
        
        # Generates a password reset token and encodes the user's ID in base64
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        reset_link = f"http://localhost:8000/auth/reset-password/{uidb64}/{token}/" # builds a clickable reset link

        try: # sends the reset link to the user's email
            send_mail(
                subject="Password Reset Request",
                message=f"Use the link below to reset your password:\n{reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,  # if sending the email fails, raise an error (don't fail silently)
            )
            return Response({"message": "Password reset link sent to your email"}, status=status.HTTP_200_OK)
        # If something goes wrong inside the try block (like email server not working, invalid credentials, or no internet),
        # Exception as e: catches the actual error and stores it in variable e and str(e): converts that error 
        # to text so it can be displayed in the response.
        except Exception as e:
            # Catch connection errors or SMTP issues
            return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny] # anyone with a valid token can reset their password

    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data) # passing in the data sent by the user to serializer for validation
        serializer.is_valid(raise_exception=True)

        try:
            # decode uid to get user
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = ChiefEditor.objects.get(pk=uid)   # use your ChiefEditor model
        except (TypeError, ValueError, OverflowError, ChiefEditor.DoesNotExist): # if any of these four types of errors occur, 
            # run the code below instead of crashing
            return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)

        # check if token is valid
        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        # reset password if token is valid
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["confirm_password"]

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

            # updates the user's password securely
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)


