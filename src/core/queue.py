

class Queue:

    """
    Queue is a class that implements a basic queue data structure, allowing for typical queue operations such as enqueue, dequeue, and priority insertion.
    It also provides methods to check if the queue is empty, retrieve the current size, and inspect the first element.

    Methods:
    - is_empty() -> bool: Returns True if the queue is empty, otherwise False.
    - enqueue(obj: object) -> None: Adds an object to the end of the queue.
    - dequeue() -> object: Removes and returns the first object from the queue. Returns None if the queue is empty.
    - enqueue_max_priority(obj: object) -> None: Adds an object to the front of the queue (priority insertion).
    - remove(obj: object) -> None: Removes the specified object from the queue, if it exists.
    - top() -> object: Returns the first object in the queue without removing it.

    Properties:
    - size (int): Returns the current size of the queue.
    - values (list): Returns the list of objects currently in the queue.

    Raises:
    - None. The methods handle queue underflow internally by checking if the queue is empty.
    """

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