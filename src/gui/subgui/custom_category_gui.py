

from src.core.sorting_task import SortingTask
from src.core.app_config_object import AppConfigurationObject
from src.core.assertion_helper import AssertionHelper
from src.scripts.custom_category_helper import CustomCategoryHelper

import tkinter as tk
from tkinter import filedialog
import os


class CustomCategoryGUI:

    """
    A graphical user interface for creating custom categories in a sorting task.

    Attributes:
    - root (tk.Tk): The main application window.
    - _sorting_task (SortingTask): The sorting task to which custom categories will be added.
    - _app_config (AppConfigurationObject): The application configuration object.
    - _target_directory (str): The directory selected for the custom category.
    - has_created_category (bool): Indicates whether a category has been created.

    Methods:
    - __init__(root: tk.Tk, sorting_task: SortingTask, app_config: AppConfigurationObject): Initializes the GUI and prompts the user to select a target directory.
    - ask_directory() -> None: Prompts the user to select a directory.
    - init_GUI() -> None: Initializes the GUI components for creating a custom category.
    - create_category() -> None: Creates a custom category based on user input.
    - on_enter(event: tk.Event) -> None: Handles the Enter key event to create a category.
    - on_escape(event: tk.Event) -> None: Handles the Escape key event to close the category window.

    Properties:
    - sorting_task: Returns the sorting task associated with the GUI.
    - app_config: Returns the application configuration.
    - target_directory: Returns the target directory for the custom category.
    - set_target_directory(new_dir: str) -> None: Sets the target directory and verifies its validity.
    """

    def __init__(self, root: tk.Tk, sorting_task: SortingTask, app_config: AppConfigurationObject) -> None:

        self.root: tk.Tk = root
        self._sorting_task: SortingTask = sorting_task
        self._app_config: AppConfigurationObject = app_config
        self._target_directory: str = None
        self.has_created_category: bool = False

        self.ask_directory()
        self.init_GUI()

    @property
    def sorting_task(self) -> SortingTask:
        return self._sorting_task
    
    @property
    def app_config(self) -> AppConfigurationObject:
        return self._app_config

    @property
    def target_directory(self) -> str:
        return self._target_directory
    
    def set_target_directory(self, new_dir: str) -> None:
        AssertionHelper.verify_filepath(new_dir)
        self._target_directory = new_dir

    @staticmethod
    def get_directory_name(path: str) -> str:
        AssertionHelper.verify_filepath(path)
        return os.path.dirname(path)


    def ask_directory(self) -> None:
        
        target_dir_path: str = filedialog.askdirectory(title="Select a directory")
        if not os.path.isdir(target_dir_path): return
        self.set_target_directory(target_dir_path)

    def init_GUI(self) -> None:

        # Préconditions pour ouvrir le GUI, sinon on return et on ouvre jamais le GUI.
        if not self.target_directory: return
        if not self.sorting_task: return
        if self.sorting_task.is_empty(): return

        bg_color: str = self.app_config.colors.background2_color
        button_color: str = self.app_config.colors.button1_color
        text_color: str = self.app_config.colors.text2_color

        self.custom_category_window: tk.Toplevel = tk.Toplevel(self.root)
        self.custom_category_window.title("Change File Name")
        self.custom_category_window.config(background=bg_color)
        self.custom_category_window.grab_set()
        self.custom_category_window.bind('<Return>', self.on_enter)
        self.custom_category_window.bind('<Escape>', self.on_escape)


        self.adding_category_window_label: tk.Label = tk.Label(
            self.custom_category_window,
            text=f"Category Name : [{self.get_directory_name(self.target_directory)}]",
            bg=bg_color, fg=text_color)
        self.category_name_entry: tk.Entry = tk.Entry(self.custom_category_window)
        self.confirm_button = tk.Button(self.custom_category_window, text="Confirm", command=self.create_category,
                                        bg=button_color, fg=text_color)
        self.cancel_button = tk.Button(self.custom_category_window, text="Cancel", command=self.custom_category_window.destroy,
                                        bg=button_color, fg=text_color)
 
        self.adding_category_window_label.grid(row=0, columnspan=2, sticky='nswe', pady=5)
        self.category_name_entry.grid(row=1, columnspan=2, sticky='nswe', pady=5, padx=3)
        self.confirm_button.grid(row=2, column=0, sticky='nswe', pady=5, padx=3)
        self.cancel_button.grid(row=2, column=1, sticky='nswe', pady=5, padx=3)

        self.root.wait_window(self.custom_category_window)

    def create_category(self) -> None:

        custom_category_name: str = self.category_name_entry.get()
        if not custom_category_name: custom_category_name = self.get_directory_name(self.target_directory)
        CustomCategoryHelper.add_custom_category(self.sorting_task, {'path': self.target_directory, 'name': custom_category_name})
        self.custom_category_window.destroy()
        self.has_created_category = True

    def on_enter(self, event: tk.Event) -> None:
        self.create_category()
    
    def on_escape(self, event: tk.Event) -> None:
        self.custom_category_window.destroy()



