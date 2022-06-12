from django.db import models


class Application(models.Model):
    """APK file model"""

    application = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200)
    package_version_code = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    owner = models.ForeignKey(
        "auth.User", related_name="applications", on_delete=models.CASCADE
    )

    def detail(self):
        return f"application: {self.application}, package_name: {self.package_name}, owner: {self.owner}"
