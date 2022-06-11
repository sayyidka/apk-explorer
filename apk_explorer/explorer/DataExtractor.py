from androguard.core.bytecodes.apk import APK, get_apkid


class DataExtractor:
    """Class for extracting data from APK file."""

    def __init__(self, file_obj) -> None:
        self.file_obj = file_obj
        self.initialize_extraction()

    def initialize_extraction(self) -> None:
        """Instantiate the necessary class for extracting data."""
        self.filepath = self.file_obj.temporary_file_path()
        self.apk = APK(self.filepath)

    def extract_data(self) -> dict:
        """Return a dictionnary with APK data."""
        apk_infos = get_apkid(self.filepath)
        application = self.filepath
        package_name = apk_infos[0]
        package_version_code = apk_infos[2]
        icon = self.apk.get_app_icon()

        return {
            "application": application,
            "package_name": package_name,
            "package_version_code": package_version_code,
            "icon": icon,
        }
