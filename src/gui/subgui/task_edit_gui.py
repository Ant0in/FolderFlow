


from src.core.app_config_object import AppConfigurationObject
from src.core.sorting_task import SortingTask
from src.scripts.yaml_helper import YAMLSafeHelper


import tkinter as tk
from tkinter import ttk, filedialog




class TaskEditGUI:

    """
    A graphical user interface for editing an existing sorting task.

    This class allows users to modify the parameters of a sorting task previously created in the application.

    Attributes:
    - root (tk.Tk): The main application window.
    - _app_config (AppConfigurationObject): The application configuration object containing visual styles and settings.
    - _sorting_task (SortingTask): The current sorting task that is being edited.

    Methods:
    - __init__(root: tk.Tk, app_config: AppConfigurationObject, sorting_task: SortingTask): Initializes the GUI with the provided application configuration and sorting task.
    - init_GUI() -> None: Sets up and configures the graphical components for editing the sorting task.

    Properties:
    - app_config: Returns the application configuration object.
    - sorting_task: Returns the current sorting task being edited.
    """

    def __init__(self, root: tk.Tk, app_config: AppConfigurationObject, sorting_task: SortingTask) -> None:

        self.root: tk.Tk = root
        self._app_config: AppConfigurationObject = app_config
        self._sorting_task: SortingTask = sorting_task

        self.init_GUI()

    @property
    def app_config(self) -> AppConfigurationObject:
        return self._app_config
    
    @property
    def sorting_task(self) -> SortingTask:
        return self._sorting_task

    def init_GUI(self) -> None:
        
        bg_color: str = self.app_config.colors.background2_color
        text_color: str = self.app_config.colors.text2_color
        button_color: str = self.app_config.colors.button1_color

        self.creating_task_window: tk.Toplevel = tk.Toplevel(self.root)
        self.creating_task_window.title("Task Edit")
        self.creating_task_window.config(background=bg_color)
        self.creating_task_window.grab_set()

        # ... code here

        self.root.wait_window(self.creating_task_window)