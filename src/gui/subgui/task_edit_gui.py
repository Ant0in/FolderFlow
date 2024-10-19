


from src.core.app_config_object import AppConfigurationObject
from src.core.sorting_task import SortingTask
from src.scripts.yaml_helper import YAMLSafeHelper


import tkinter as tk
from tkinter import ttk, filedialog




class TaskEditGUI:

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