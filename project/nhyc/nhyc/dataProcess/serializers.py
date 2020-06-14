from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Member, MemberTrend

# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("memberId", "name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        member = Member.objects.create_user(
            memberId=validated_data["memberId"],
            password=validated_data["password"],
            name=validated_data["name"],
            email=validated_data["email"],
        )
        memberTrend = MemberTrend(member=member)
        memberTrend.save()
        return member


# 접속 유지중인지 확인
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("memberId", "name")


# 로그인
class LoginUserSerializer(serializers.Serializer):
    memberId = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")