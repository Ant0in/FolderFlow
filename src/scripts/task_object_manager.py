

from src.core.sorting_task import SortingTask
from src.core.file_objects import FileObject, VideoObject, ImageObject
from src.core.assertion_helper import AssertionHelper
from src.scripts.yaml_helper import YAMLSafeHelper

import os
import pathlib



class SortingTaskObjectManager:

    """
    A manager class for handling sorting tasks and file objects.

    Methods:
    - get_file_extension(file: str) -> str:
    Returns the file extension of a given file if it exists.
    - create_file_object(file: str, valid_ext: dict[str: list[str]]) -> FileObject:
    Creates a FileObject based on the file extension and valid extensions.
    - create_task_object(
        files: list[str] = None,
        reviewed_files: list[str] = None,
        custom_categories: list = None,
        supported_ext_fp: str = None,
        init_file_count: int = None,
        task_path: str = None,
    ) -> SortingTask:
    Creates a SortingTask object from the given files and configuration.
    - dump_task_data(task: SortingTask, task_folder: str, taskname: str) -> bool:
    Saves the sorting task data to a YAML file in the specified folder.
    - load_task_data(task_path: str, supported_ext_fp: str) -> SortingTask:
    Loads a sorting task from a YAML file and returns a SortingTask object.
    """

    @staticmethod
    def get_file_extension(file: str) -> str:
        
        if not file: return None
        
        # Si le fichier est valide, alors on récupère son extension et on return.
        if os.path.isfile(file):
            return os.path.splitext(file)[-1]

    @staticmethod
    def create_file_object(file: str, valid_ext: dict[str: list[str]]) -> FileObject:

        file_ext: str = SortingTaskObjectManager.get_file_extension(file)
        task_obj: FileObject = None

        if file_ext in valid_ext.get('image_extensions', []): task_obj = ImageObject(file)
        elif file_ext in valid_ext.get('video_extensions', []): task_obj = VideoObject(file)
        else: raise NotImplementedError(f'Unknown ext {file_ext}')

        return task_obj

    @staticmethod
    def create_task_object(
        files: list[str] = None,
        reviewed_files: list[str] = None,
        custom_categories: list = None,
        supported_ext_fp: str = None,
        init_file_count: int = None,
        task_path: str = None,
    ) -> SortingTask:

        AssertionHelper.verify_file_extension(supported_ext_fp, '.yaml')
        valid_ext: dict = YAMLSafeHelper.safe_load(supported_ext_fp)
        task: SortingTask = SortingTask(files=None, reviewed_files=None, custom_categories=custom_categories)


        # Pour chaque file, on crée son fileobject associé, et on l'ajoute à la SortingTask si il n'est pas None.
        if files:
            for file in files:
                task_obj: FileObject = SortingTaskObjectManager.create_file_object(file=file, valid_ext=valid_ext)
                if task_obj: task.file_enqueue(task_obj)

        # Pour chaque reviewed file, on crée son fileobject associé, et on l'ajoute à la SortingTask si il n'est pas None.
        if reviewed_files:
            for reviewed_file in reviewed_files:
                task_obj: FileObject = SortingTaskObjectManager.create_file_object(file=reviewed_file, valid_ext=valid_ext)
                if task_obj: task.reviewed_files.push(task_obj)

        if init_file_count: task.set_init_file_count(init_file_count)
        if task_path: task.set_path(task_path)

        return task
    
    @staticmethod
    def dump_task_data(task: SortingTask, task_folder: str, taskname: str) -> bool:

        # On initialise l'ADT qui contiendra les informations à sauvegarder.
        task_data: dict[str: list] = {
            'custom_categories': [],
            'files': [],
            'reviewed_files': [],
            'init_file_count': None,
        }

        # On récupère dans l'ordre les catégories custom crées par l'utilisateur, les
        # fichiers à trier et enfin le dernier fichier trié s'il existe.
        for custom_category in task.get_custom_categories():
            custom_category.pop('button_ref', None)
            task_data['custom_categories'].append(custom_category)

        for file in task.files.values:
            task_data['files'].append(file.path)
        for reviewed_file in task.reviewed_files.values:
            task_data['reviewed_files'].append(reviewed_file.path)
        
        if task.init_file_count:
            task_data['init_file_count'] = task.init_file_count

        # On crée ensuite le path correct vers le fichier, puis on vérifie qu'il est valide et enfin on dump les données.
        task_path: str = os.path.join(task_folder, taskname)
        if not os.path.exists(task_path):
            pathlib.Path.touch(task_path)
        AssertionHelper.verify_file_extension(task_path, '.yaml')
        YAMLSafeHelper.safe_dump(task_path, task_data)

        return True

    @staticmethod
    def load_task_data(task_path: str, supported_ext_fp: str) -> SortingTask:

        # On vérifie le task_path avant de le load.
        AssertionHelper.verify_file_extension(task_path, '.yaml')
        task_data: dict = YAMLSafeHelper.safe_load(task_path)

        valid_files: list = []
        invalid_files: list = []
        valid_prev_files: list = []
        invalid_prev_files: list = []
        valid_custom_categories: list = []
        invalid_custom_categories: list = []

        # On parcourt les fichiers dans les données du load .yaml et on les récupère 
        # si les path sont encore valides (Les fichiers n'ont pas changé de place / été supprimés).

        for file in task_data['files']:
            if os.path.exists(file): valid_files.append(file)
            else: invalid_files.append(file)

        for prev_file in task_data['reviewed_files']:
            if os.path.exists(prev_file): valid_prev_files.append(prev_file)
            else: invalid_prev_files.append(prev_file)

        for custom_category in task_data['custom_categories']:
            if os.path.exists(custom_category['path']): valid_custom_categories.append(custom_category)
            else: invalid_custom_categories.append(custom_category)

        # On crée finalement la SortingTask afin de la return.
        task: SortingTask = SortingTaskObjectManager.create_task_object(
            files=valid_files,
            reviewed_files=valid_prev_files,
            custom_categories=valid_custom_categories,
            supported_ext_fp=supported_ext_fp,
            init_file_count=task_data['init_file_count'],
            task_path=task_path
        )

        return task
