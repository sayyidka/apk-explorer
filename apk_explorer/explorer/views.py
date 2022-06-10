from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from explorer.models import Application
from explorer.serializers import ApplicationSerializer, CreatorSerializer
from rest_framework.parsers import MultiPartParser
from androguard.core.bytecodes.apk import APK, get_apkid

# Create your views here.
class Applications(APIView):
    parser_classes = [MultiPartParser]

    def get(self):
        applications = Application.objects.all().order_by("package_name")
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Get file from request
        file_obj = request.FILES["file"]
        filepath = file_obj.temporary_file_path()
        a = APK(filepath)
        apk_infos = get_apkid(filepath)

        # Extract file content
        application = file_obj.temporary_file_path()
        package_name = apk_infos[0]
        package_version_code = apk_infos[2]
        icon = a.get_app_icon()

        # todo : save into DB
        data = {
            "application": application,
            "package_name": package_name,
            "package_version_code": package_version_code,
            "icon": icon,
        }
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetail(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        app = get_object_or_404(Application, id=id)
        serializer = ApplicationSerializer(app)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")
        apk_to_update = get_object_or_404(Application, id=id)

        # Get file from request
        file_obj = request.FILES["file"]
        filepath = file_obj.temporary_file_path()
        a = APK(filepath)
        apk_infos = get_apkid(filepath)

        # Extract file content
        application = file_obj.temporary_file_path()
        package_name = apk_infos[0]
        package_version_code = apk_infos[2]
        icon = a.get_app_icon()

        # todo : save into DB
        data = {
            "application": application,
            "package_name": package_name,
            "package_version_code": package_version_code,
            "icon": icon,
        }
        serializer = ApplicationSerializer(apk_to_update, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        app = get_object_or_404(Application, id=id)
        app.delete()
        return Response(
            "Application removed successfully !", status=status.HTTP_204_NO_CONTENT
        )


class Creators(APIView):
    def get(self):
        creators = Creators.objects.all().order_by("username")
        serializer = CreatorSerializer(creators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass
