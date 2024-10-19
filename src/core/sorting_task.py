

from src.core.file_objects import FileObject
from src.core.queue import Queue
from src.core.stack import Stack


class SortingTask:

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

