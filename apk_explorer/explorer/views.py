from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from explorer.models import Application
from explorer.CustomPermissions import IsOwnerOrReadOnly, IsUserOrReadOnly
from explorer.serializers import ApplicationSerializer, UserSerializer
from explorer.DataExtractor import DataExtractor


class Applications(APIView):
    """View to all applications.

    * Requires token authentication for uploading APK files.
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        """
        Return a list of applications.
        """
        applications = Application.objects.all().order_by("package_name")
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Upload an application from an APK file.
        The package_name must not already exist in DB and the same version cannot be
        uploaded twice.
        """
        # Get file from request
        file_obj = request.FILES["file"]

        # Extract file content
        data_extractor = DataExtractor(file_obj)
        data = data_extractor.extract_data()

        # Check if an package with the same name already exists
        applications = Application.objects.all()
        same_package_name = applications.filter(package_name=data["package_name"])
        if same_package_name:
            package = same_package_name.first()
            if package.owner != request.user:
                return Response(
                    "An APK file with the same package_name already exists.",
                    status=status.HTTP_409_CONFLICT,
                )
            if package.package_version_code == data["package_version_code"]:
                return Response(
                    "An APK file with the same package_version_code already exists.",
                    status=status.HTTP_409_CONFLICT,
                )

        # Save into DB
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetail(APIView):
    """View to single application.

    * Requires token authentication for updating and removing APK files.
    """

    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, *args, **kwargs):
        """
        Return the selected application.
        """
        id = kwargs.get("id")
        app = get_object_or_404(Application, id=id)
        serializer = ApplicationSerializer(app)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Update the selected application.
        The application must belong to the user who make the request.
        """
        id = kwargs.get("id")
        apk_to_update = get_object_or_404(Application, id=id)
        self.check_object_permissions(request, apk_to_update)

        # Get file from request
        file_obj = request.FILES["file"]

        # Extract file content
        data_extractor = DataExtractor(file_obj)
        data = data_extractor.extract_data()

        # Save into DB
        serializer = ApplicationSerializer(apk_to_update, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Remove the selected application.
        The application must belong to the user who make the request.
        """
        id = kwargs.get("id")
        app = get_object_or_404(Application, id=id)
        self.check_object_permissions(request, app)
        app.delete()
        return Response(
            "Application removed successfully !", status=status.HTTP_204_NO_CONTENT
        )


class Users(APIView):
    """View to all users."""

    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        """
        Return a list of users.
        """
        users = User.objects.all().order_by("username")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersRegister(APIView):
    """View for user registration."""

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Create a new user.
        """
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
    """View to single user.

    * Requires token authentication for updating and deleting user.
    """

    permission_classes = (IsAuthenticatedOrReadOnly, IsUserOrReadOnly)

    def get(self, request, *args, **kwargs):
        """
        Return the selected user.
        """
        userid = kwargs.get("userid")
        user = get_object_or_404(User, id=userid)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        Update the selected user.
        The user to update must be the same as the one who make the request.
        """
        userid = kwargs.get("userid")
        user = get_object_or_404(User, id=userid)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(data="Invalid parameter", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Remove the selected user.
        The user to remove must be the same as the one who make the request.
        """
        userid = kwargs.get("userid")
        user = get_object_or_404(User, id=userid)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(
            "User removed successfully !", status=status.HTTP_204_NO_CONTENT
        )
