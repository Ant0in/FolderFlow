

class Queue:

    def __init__(self, init_values: list[object]) -> None:

        self._values: list = init_values if init_values else []
        self._size: int = len(self.values)

    @property
    def size(self) -> int:
        return self._size
    
    def set_size(self, n: int) -> None:
        self._size = n

    @property
    def values(self) -> list:
        return self._values
    
    def is_empty(self) -> bool:
        return self.size == 0
    
    def enqueue(self, obj: object) -> None:
        self.set_size(self.size + 1)
        self.values.append(obj)

    def dequeue(self) -> object:
        if not self.is_empty():
            self.set_size(self.size - 1)
            return self.values.pop(0)
    
    def enqueue_max_priority(self, obj: object) -> None:
        self.set_size(self.size + 1)
        self.values.insert(0, obj)
    
    def remove(self, obj: object) -> None:
        if obj in self.values:
            self.values.remove(obj)
            self.set_size(self.size - 1)

    def top(self) -> object:
        if not self.is_empty():
            return self.values[0]