from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from androguard.core.bytecodes.apk import APK, get_apkid
from explorer.models import Application
from explorer.CustomPermissions import IsOwnerOrReadOnly, IsUserOrReadOnly
from explorer.serializers import ApplicationSerializer, UserSerializer


class Applications(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
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

        # Check if an package with the same name already exists
        applications = Application.objects.all()
        same_package_name = applications.filter(package_name=package_name)
        if same_package_name:
            package = same_package_name.first()
            if package.owner != request.user:
                return Response(
                    "An APK file with the same package_name already exists.",
                    status=status.HTTP_409_CONFLICT,
                )
            if package.package_version_code == package_version_code:
                return Response(
                    "An APK file with the same package_version_code already exists.",
                    status=status.HTTP_409_CONFLICT,
                )

        # Save into DB
        data = {
            "application": application,
            "package_name": package_name,
            "package_version_code": package_version_code,
            "icon": icon,
        }
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            print(serializer)
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        app = get_object_or_404(Application, id=id)
        serializer = ApplicationSerializer(app)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")
        apk_to_update = get_object_or_404(Application, id=id)
        self.check_object_permissions(request, apk_to_update)

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

        # Save into DB
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
        self.check_object_permissions(request, app)
        app.delete()
        return Response(
            "Application removed successfully !", status=status.HTTP_204_NO_CONTENT
        )


class Users(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        users = User.objects.all().order_by("username")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersRegister(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user_obj = request.data
        data = {
            "username": user_obj["username"],
            "password": user_obj["password"],
            "email": user_obj["email"],
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsUserOrReadOnly)

    def get(self, request, *args, **kwargs):
        userid = kwargs.get("userid")
        user = get_object_or_404(User, id=userid)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        userid = kwargs.get("userid")
        user = get_object_or_404(User, id=userid)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(data="Invalid parameter", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        userid = kwargs.get("userid")
        user = get_object_or_404(User, id=userid)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(
            "User removed successfully !", status=status.HTTP_204_NO_CONTENT
        )
