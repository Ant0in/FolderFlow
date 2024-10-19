

from src.core.file_objects import FileObject
from src.core.queue import Queue
from src.core.stack import Stack


class SortingTask:

    """
    SortingTask is a class designed to manage and organize a collection of files for sorting tasks. 
    It utilizes a Queue to hold files that need to be sorted and a Stack to keep track of files that have already been reviewed. 
    Additionally, it supports custom categorization for sorting.

    Attributes:
    - files (Queue): A queue that holds files pending sorting.
    - reviewed_files (Stack): A stack that contains files that have been reviewed.
    - custom_categories (list): A list of custom categories for sorting files.
    - path (str | None): The path associated with the sorting task.
    - init_file_count (int | None): The initial count of files to be sorted.

    Methods:
    - is_empty() -> bool: Returns True if there are no files to sort, otherwise False.
    - file_enqueue(file: FileObject) -> None: Adds a file to the queue for sorting.
    - file_dequeue() -> FileObject: Removes the next file from the queue and pushes it onto the reviewed files stack.
    - get_current_file() -> FileObject: Returns the file currently at the front of the queue without removing it.
    - get_most_recent_reviewed_file() -> FileObject: Returns the most recently reviewed file from the stack without removing it.
    - restore_previous_reviewed_file() -> None: Restores the most recently reviewed file back to the front of the queue.
    - get_custom_categories(sort_by_name: bool = True) -> list: Returns the list of custom categories, sorted by name if specified.
    - add_custom_categories(*new_categories: dict) -> None: Adds new custom categories to the existing list.
    - remove_custom_category(target: dict) -> None: Removes a specified custom category from the list.
    - clear_custom_categories() -> None: Clears all custom categories from the list.

    Raises:
    - AssertionError: If a new category added is not a dictionary.
    """

    def __init__(self,
            files: list[FileObject] | None = None,
            reviewed_files: list[FileObject] | None = None,
            custom_categories: list[dict[str: str]] | None = None
        ) -> None:

        # SortingTask possède une Queue pour les fichiers à trier et un Stack pour les fichiers déjà triés.
        self._files: Queue = Queue(init_values=files)
        self._reviewed_files: Stack = Stack(init_values=reviewed_files)
        self._custom_categories: list[dict[str: str]] = custom_categories if custom_categories else []

        self._path: str | None = None
        self._init_file_count: int | None = None
        
    @property
    def files(self) -> Queue:
        return self._files
    
    @property
    def reviewed_files(self) -> Stack:
        return self._reviewed_files

    @property
    def size(self) -> int:
        return self.files.size

    @property
    def reviewed_size(self) -> int:
        return self.reviewed_files.size()

    @property
    def path(self) -> str:
        return self._path
    
    def set_path(self, new_path: str) -> None:
        self._path = new_path

    @property
    def init_file_count(self) -> int:
        return self._init_file_count
    
    def set_init_file_count(self, c: int) -> None:
        self._init_file_count = c
    
    def is_empty(self) -> bool:
        return self.size == 0

    def file_enqueue(self, file: FileObject) -> None:
        self.files.enqueue(file)

    def file_dequeue(self) -> FileObject:

        p: FileObject = self.files.dequeue()
        if p:
            self.reviewed_files.push(p)
            return p
        
    def get_current_file(self) -> FileObject:
        return self.files.top()
    
    def get_most_recent_reviewed_file(self) -> FileObject:
        return self.reviewed_files.top()
    
    def restore_previous_reviewed_file(self) -> None:

        p: FileObject = self.reviewed_files.pop()
        if p:
            self.files.enqueue_max_priority(p)

    def get_custom_categories(self, sort_by_name: bool = True) -> list[dict[str: str]]:

        return sorted(self._custom_categories, key=lambda c: c['name']) \
            if sort_by_name else self._custom_categories
    
    def add_custom_categories(self, *new_categories: dict[str: str]) -> None:
        for nc in new_categories:
            assert isinstance(nc, dict)
            self._custom_categories.append(nc)

    def remove_custom_category(self, target: dict) -> None:
        
        for custom_category in self.get_custom_categories():
            if custom_category['name'] == target['name'] and \
                custom_category['path'] == target['path']:
                self._custom_categories.remove(custom_category)
                break

    def clear_custom_categories(self) -> None:
        self._custom_categories.clear()

