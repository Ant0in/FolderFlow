

from src.scripts.task_object_manager import SortingTaskObjectManager
from src.core.sorting_task import SortingTask
from src.core.file_objects import FileObject
from src.scripts.crawler import Crawler

from tkinter import filedialog
import os



class SortingTaskDataManager:

    """
    A manager class for creating, loading, and saving sorting tasks.

    Methods:
    - create_task(task_path: str, selected_ext: list[str], local_mode: bool, shuffle_mode: bool, config_folder: str) -> SortingTask:
    Creates a new sorting task by crawling a specified folder for files of selected extensions.
    - load_task(supported_extension_fp: str) -> SortingTask:
    Loads a sorting task from a YAML file selected by the user.
    - save_task(task: SortingTask, task_fp: str) -> bool:
    Saves the current sorting task to a specified file path, returning the success status.
    - save_as_task(task: SortingTask) -> bool:
    Opens a dialog for the user to specify a file path to save the current sorting task.
    """

    @staticmethod
    def create_task(task_path: str, selected_ext: list[str], local_mode: bool, shuffle_mode: bool, config_folder: str) -> SortingTask:

        crwl: Crawler = Crawler(*selected_ext)
        files: list[FileObject] = crwl.crawl_folder(task_path, local_only=local_mode, shuffle=shuffle_mode)
        task: SortingTask = SortingTaskObjectManager.create_task_object(
            files=files,
            reviewed_files=None,
            custom_categories=None,
            supported_ext_fp=config_folder,
            init_file_count=None,
            task_path=None)

        task.set_init_file_count(task.size)
        
        return task

    @staticmethod
    def load_task(supported_extension_fp: str) -> SortingTask:

        file_path: str = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("YAML files", "*.yaml")]
        )

        if file_path: return SortingTaskObjectManager.load_task_data(file_path, supported_extension_fp)

    @staticmethod
    def save_task(task: SortingTask, task_fp: str) -> bool:

        if not task_fp: return SortingTaskDataManager.save_as_task(task)

        filename: str = os.path.basename(task_fp)
        dirname: str = os.path.dirname(task_fp)
        status: bool = SortingTaskObjectManager.dump_task_data(task, dirname, filename)
        task.set_path(task_fp)
        return status

    @staticmethod
    def save_as_task(task: SortingTask) -> bool:
  
        file_path: str = filedialog.asksaveasfilename(
            title="Save YAML file",
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml")]
        )

        # Une fois qu'on a un PATH, il s'agit d'un dump normal.
        if file_path: 
            status: bool = SortingTaskDataManager.save_task(task, file_path)
            return status
        else: return False


