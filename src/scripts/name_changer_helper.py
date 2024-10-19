

from src.core.file_objects import FileObject
from src.core.sorting_task import SortingTask

import os
import string
import random



class FilenameManager:

    @staticmethod
    def rename_file(sorting_task: SortingTask, new_name: str) -> None:

        if sorting_task.is_empty(): return

        current: FileObject = sorting_task.get_current_file()
        current.close()  # le videocap pourrait monopoliser le fichier, donc on le ferme
        new_fp: str = os.path.join(current.dirname, new_name) + current.extension
        os.rename(current.path, new_fp)
        current.set_new_path(new_fp)

    @staticmethod
    def rename_file_random(sorting_task: SortingTask, random_length: int) -> None:

        characters: str = string.ascii_uppercase + string.digits
        random_name: str = ''.join(random.choices(characters, k=random_length))
        FilenameManager.rename_file(sorting_task, random_name)