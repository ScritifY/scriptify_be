from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, RegisterSerializer


# 회원가입
class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ['post']


# 유저 정보 조회
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_object(self):
        return self.request.user