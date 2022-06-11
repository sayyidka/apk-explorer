from django.contrib.auth.models import User
from rest_framework import serializers
from explorer.models import Application


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ApplicationSerializer(serializers.ModelSerializer):
    application = serializers.CharField(max_length=200)
    package_name = serializers.CharField(max_length=200)
    package_version_code = serializers.CharField(max_length=200)
    icon = serializers.CharField(max_length=200)
    owner = UserShortSerializer(read_only=True)

    class Meta:
        model = Application
        fields = (
            "application",
            "package_name",
            "package_version_code",
            "icon",
            "owner",
        )


class ApplicationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "application",
            "package_name",
            "package_version_code",
        )


class UserSerializer(serializers.ModelSerializer):
    applications = ApplicationShortSerializer(many=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )
        return user

    class Meta:
        model = User
        fields = ("id", "username", "applications")
