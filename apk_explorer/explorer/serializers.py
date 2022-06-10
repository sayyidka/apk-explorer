from dataclasses import fields
from unittest.util import _MAX_LENGTH
from matplotlib.pyplot import cla
from rest_framework import serializers
from explorer.models import Application, Creator


class ApplicationSerializer(serializers.ModelSerializer):
    application = serializers.CharField(max_length=200)
    package_name = serializers.CharField(max_length=200)
    package_version_code = serializers.CharField(max_length=200)
    icon = serializers.CharField(max_length=200)

    class Meta:
        model = Application
        fields = ("application", "package_name", "package_version_code", "icon")


class CreatorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)

    class Meta:
        model = Creator
        fields = "username"
