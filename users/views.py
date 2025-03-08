from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from users.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

class RegisterView(APIView):
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User registerd Successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        identifier = request.data.get("username_or_email")  # This is what the frontend should send
        password = request.data.get("password")

        if not identifier or not password:
            return Response({"error": "Both username or email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the identifier is an email or username
            if '@' in identifier:
                # Check by email if the identifier contains '@'
                user = CustomUser.objects.get(email=identifier)
                username = user.username  # Get the username from the email
            else:
                # Otherwise, treat it as a username
                username = identifier
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate the user using the username and password
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                "message": "Login Successful 🎉"
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

KHALTI_API_URL = "https://dev.khalti.com/api/v2/epayment/initiate/"
KHALTI_SECRET_KEY = "Key 8ec002aace27429dad2b86d027ddf962" 

@csrf_exempt  # Remove in production
def khalti(request):
      
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            payload = {
                "return_url": "http://localhost:3000/paymentSucess",
                "website_url": "https://localhost:3000/profile/",
                "amount": data.get("amount"),  # Amount in paisa (1000 = 10 NPR)
                "purchase_order_id": data.get("purchase_order_id"),
                "purchase_order_name": data.get("purchase_order_name", "Test Order"),
                "customer_info": {
                    "name": data.get("name"),
                    "email": data.get("email", "test@khalti.com"),
                    "phone": data.get("phone", "9800000001"),
                }
            }

            headers = {
                "Authorization":f"{KHALTI_SECRET_KEY}",
                "Content-Type": "application/json",
            }

            response = requests.post(KHALTI_API_URL, headers=headers, json=payload)

            return JsonResponse(response.json(), status=response.status_code)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
