from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *


@api_view(['POST'])
def activation_user_email(request):
    user_email = request.data['email']
    verify_code = request.data['verify_code']

    user = CustomUser.objects.get(email=user_email)
    if user.verify_code == verify_code:
        user.is_active = True
        user.save()
        return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)

    return Response({'message': 'Invalid verify_code.'}, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.

# class UserProfileViewSet(ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = serializers.UserProfileSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         return UserProfile.objects.filter(user_id=self.request.user.id)
    
#     def get_serializer_context(self):
#         return {
#             'user_id':self.request.user.id
#         }


    # @action(detail=False,methods=['GET', 'PUT', 'POST'], permission_classes=[IsAuthenticated])
    # def me(self, request):
    #     user_profile = UserProfile.objects.get(user_id=request.user.id)
    #     if request.method == 'GET':
    #         serializer = serializers.UserProfileSerializer(user_profile)
    #         return Response(data=serializer.data)
    #     elif request.method == 'PUT':
    #         serializer = serializers.UserProfileSerializer(user_profile, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     elif request.method == 'POST':

        
            



