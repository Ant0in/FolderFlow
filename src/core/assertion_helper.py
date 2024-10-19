

import os


class AssertionHelper:

    @staticmethod
    def verify_filepath(fp: str) -> None:
        assert isinstance(fp, str), f"[E] L'objet '{fp}' n'est pas du bon type (string). type={type(fp)}"
        assert os.path.exists(fp), f"[E] Le chemin {fp} n'est pas valide ou n'existe pas."

    @staticmethod
    def verify_file_extension(fp: str, extension: str) -> None:
        AssertionHelper.verify_filepath(fp=fp)
        assert os.path.splitext(fp)[-1] == extension, f"[E] Le fichier {os.path.basename(fp)} n'est pas un fichier {extension}."


