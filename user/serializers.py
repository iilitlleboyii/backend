# from django.contrib.auth import get_user_model
from .models import User, Role
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework import exceptions


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    登录
    """

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username

        return token

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                "用户名或密码错误",
                "authentication_failed",
            )

        data = {}

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        # 添加预期的数据
        data['userInfo'] = UserProfileSerializer(instance=self.user).data
        if data['userInfo']['is_superuser']:
            data['permissions'] = ['*:*:*']
            data['roles'] = ['admin']
        else:
            data['permissions'] = []
            data['roles'] = []

        return data


class UserAuthSerializer(ModelSerializer):
    """
    注册
    """

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )


class UserProfileSerializer(ModelSerializer):
    """
    获取登录用户信息
    """

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'nickname',
            'telephone',
            'email',
            'is_staff',
            'is_superuser',
        )


class UserSerializer(ModelSerializer):
    """
    用户表
    """

    class Meta:
        model = User
        exclude = (
            'password',
            'first_name',
            'last_name',
            'groups',
            'user_permissions',
        )


class RoleSerializer(ModelSerializer):
    """
    角色表
    """

    class Meta:
        model = Role
        fields = '__all__'
