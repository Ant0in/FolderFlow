

class Stack:

    """
    Stack is a class that implements a basic stack data structure, allowing for standard stack operations such as push, pop, and priority insertion.
    It provides methods to check if the stack is empty, retrieve the current size, and inspect the top element.

    Methods:
    - is_empty() -> bool: Returns True if the stack is empty, otherwise False.
    - push(obj: object) -> None: Adds an object to the top of the stack.
    - pop() -> object: Removes and returns the top object from the stack. Returns None if the stack is empty.
    - push_lowest_priority(obj: object) -> None: Adds an object to the bottom of the stack (lowest priority).
    - remove(obj: object) -> None: Removes the specified object from the stack, if it exists.
    - top() -> object: Returns the top object in the stack without removing it.

    Properties:
    - size (int): Returns the current size of the stack.
    - values (list): Returns the list of objects currently in the stack.

    Raises:
    - None. The methods handle stack underflow internally by checking if the stack is empty.
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
    
    def push(self, obj: object) -> None:
        self.set_size(self.size + 1)
        self.values.append(obj)

    def pop(self) -> object:

        if not self.is_empty():
            self.set_size(self.size - 1)
            return self.values.pop(-1)
    
    def push_lowest_priority(self, obj: object) -> object:
        self.set_size(self.size + 1)
        self.values.insert(0, obj)

    def remove(self, obj: object) -> None:
        if obj in self.values:
            self.values.remove(obj)
            self.set_size(self.size - 1)

    def top(self) -> object:
        if not self.is_empty():
            return self.values[-1]