from django.db import models

# Create your models here.
class Application(models.Model):
    application = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200)
    package_version_code = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    owner = models.ForeignKey(
        "auth.User", related_name="applications", on_delete=models.CASCADE
    )
