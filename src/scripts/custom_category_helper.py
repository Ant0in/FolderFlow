

from src.core.sorting_task import SortingTask
from src.core.file_objects import FileObject

from tkinter import messagebox, filedialog
import os
import shutil



class CustomCategoryHelper:
    
    """
    A helper class for managing custom categories in a SortingTask.

    Methods:
    - delete_custom_category(sorting_task: SortingTask, custom_category: dict) -> None: Removes a custom category from the sorting task.
    - add_custom_category(sorting_task: SortingTask, custom_category: dict) -> None: Adds a new custom category to the sorting task.
    - move_file_into_category(sorting_task: SortingTask, custom_category: dict) -> bool: Moves the currently selected file into the specified custom category.
    - add_custom_categories_from_dir(sorting_task: SortingTask) -> bool: Adds custom categories from a selected directory.
    """

    @staticmethod
    def delete_custom_category(sorting_task: SortingTask, custom_category: dict) -> None:
        sorting_task.remove_custom_category(custom_category)

    @staticmethod
    def add_custom_category(sorting_task: SortingTask, custom_category: dict) -> None:
        sorting_task.add_custom_categories(custom_category)

    @staticmethod
    def move_file_into_category(sorting_task: SortingTask, custom_category: dict) -> bool:

        current: FileObject = sorting_task.get_current_file()
        current.close()

        new_directory: str = os.path.join(custom_category['path'], current.filename)
        
        # Ce fichier existe déjà.
        if os.path.exists(new_directory):
            messagebox.showwarning(message=f'File with the same name already exist in given directory (@ {new_directory})')
            return False

        shutil.move(current.path, new_directory)
        current.set_new_path(new_directory)
        return True
    
    @staticmethod
    def add_custom_categories_from_dir(sorting_task: SortingTask) -> bool:
        
        root: str = filedialog.askdirectory()
        if not root: return False

        categories: list = [{'path': os.path.join(root, subfolder), 'name': subfolder} for subfolder in os.listdir(root)]
        if not categories: return False

        sorting_task.clear_custom_categories()
        sorting_task.add_custom_categories(*categories)
        return True

