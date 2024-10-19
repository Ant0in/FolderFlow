

import os


class AssertionHelper:

    """
    AssertionHelper is a utility class that provides static methods for verifying file paths and extensions.
    It helps ensure that file paths are valid and that files have the expected extension, raising assertions
    if any condition is not met.

    Methods:
    - verify_filepath(fp: str): Verifies that the provided file path is a string and exists in the filesystem.
    - verify_file_extension(fp: str, extension: str): Ensures the file at the given path has the specified file extension,
    and that the file path itself is valid.

    Raises:
    - AssertionError: If the file path does not exist, is not a string, or if the file extension does not match.
    """

    @staticmethod
    def verify_filepath(fp: str) -> None:
        assert isinstance(fp, str), f"[E] L'objet '{fp}' n'est pas du bon type (string). type={type(fp)}"
        assert os.path.exists(fp), f"[E] Le chemin {fp} n'est pas valide ou n'existe pas."

    @staticmethod
    def verify_file_extension(fp: str, extension: str) -> None:
        AssertionHelper.verify_filepath(fp=fp)
        assert os.path.splitext(fp)[-1] == extension, f"[E] Le fichier {os.path.basename(fp)} n'est pas un fichier {extension}."


