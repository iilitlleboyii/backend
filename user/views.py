from .models import User
from .filtersets import UserFilterSet
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, UserAuthSerializer, UserProfileSerializer

from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


@permission_classes([AllowAny])
class LoginView(TokenObtainPairView):
    """
    账号密码登录
    """
    serializer_class = CustomTokenObtainPairSerializer


@permission_classes([AllowAny])
class RegisterView(APIView):
    """
    注册用户
    """

    def post(self, request):
        req_data = request.data
        username = req_data.get('username')
        password = req_data.get('password')
        email = req_data.get('email')
        telephone = req_data.get('phoneNumber')

        if User.objects.filter(username=username).exists():
            return Response(data={'message': '该用户名已存在'},
                            status=status.HTTP_403_FORBIDDEN)

        user_data = {'username': username, 'password': make_password(password)}

        # 前端暂时隐藏了邮箱和手机号码
        if email:
            user_data['email'] = email
        if telephone:
            user_data['telephone'] = telephone

        user_serializer = UserAuthSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data={'message': '注册成功'}, status=status.HTTP_200_OK)

        return Response(data={'message': user_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    获取登录用户信息
    """

    def get(self, request):
        user = UserProfileSerializer(instance=request.user)
        return Response(data=user.data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    """
    用户表
    """

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filterset_class = UserFilterSet
    ordering_fields = ['id', 'date_joined', 'last_login']
