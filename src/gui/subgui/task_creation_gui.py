

from src.core.app_config_object import AppConfigurationObject
from src.core.sorting_task import SortingTask
from src.scripts.task_data_manager import SortingTaskDataManager
from src.scripts.yaml_helper import YAMLSafeHelper


import tkinter as tk
from tkinter import ttk, filedialog




class TaskCreationGUI:

    """
    A graphical user interface for creating a sorting task with customizable file selection options.

    Attributes:
    - root (tk.Tk): The main application window.
    - _app_config (AppConfigurationObject): The application configuration object.
    - _supported_extensions_fp (str): The file path to the YAML file containing supported file extensions.
    - _supported_extensions (dict[str: list[str]]): A dictionary of supported file extensions loaded from the YAML file.
    - _sorting_task (SortingTask): The current sorting task created by the user.

    Methods:
    - __init__(root: tk.Tk, app_config: AppConfigurationObject, supported_extensions_fp: str): Initializes the GUI and sets up the window and components.
    - init_GUI() -> None: Initializes and configures the GUI components for creating a sorting task.
    - select_filesource_folder() -> None: Opens a dialog to select the folder containing files to sort.
    - confirm_task_creation() -> None: Creates a new sorting task with the specified options and closes the window.
    - on_enter(event: tk.Event) -> None: Handles the Enter key event to confirm the task creation.
    - on_escape(event: tk.Event) -> None: Closes the task creation window.

    Properties:
    - app_config: Returns the application configuration object.
    - supported_extensions: Returns a dictionary of supported file extensions.
    - supported_extensions_filepath: Returns the file path of the supported extensions YAML file.
    - sorting_task: Returns the currently created sorting task.
    """

    def __init__(self, root: tk.Tk, app_config: AppConfigurationObject, supported_extensions_fp: str) -> None:

        self.root: tk.Tk = root
        self._app_config: AppConfigurationObject = app_config
        self._supported_extensions_fp: str = supported_extensions_fp
        self._supported_extensions: dict[str: list[str]] = YAMLSafeHelper.safe_load(supported_extensions_fp)
        self._sorting_task: SortingTask = None
        self.init_GUI()

    @property
    def app_config(self) -> AppConfigurationObject:
        return self._app_config
    
    @property
    def supported_extensions(self) -> dict[str: list[str]]:
        return self._supported_extensions

    @property
    def supported_extensions_filepath(self) -> str:
        return self._supported_extensions_fp

    @property
    def sorting_task(self) -> SortingTask:
        return self._sorting_task

    def set_sorting_task(self, task: SortingTask) -> None:
        self._sorting_task = task

    def init_GUI(self) -> None:

        bg_color: str = self.app_config.colors.background2_color
        text_color: str = self.app_config.colors.text2_color
        button_color: str = self.app_config.colors.button1_color

        self.creating_task_window: tk.Toplevel = tk.Toplevel(self.root)
        self.creating_task_window.title("Task Creation")
        self.creating_task_window.config(background=bg_color)
        self.creating_task_window.grab_set()
        self.creating_task_window.bind('<Return>', self.on_enter)
        self.creating_task_window.bind('<Escape>', self.on_escape)
    
        style: ttk.Style = ttk.Style()
        style.configure('TLabel', background=bg_color, foreground=text_color)
        style.configure('TCheckbutton', background=bg_color, foreground=text_color)
        style.configure('TButton', background=button_color, foreground=text_color)

        self.extensions_check_vars: dict[str: tk.BooleanVar] = {}

        for extension_sort, extensions in self.supported_extensions.items():

            extension_sort_frame: tk.Frame = tk.Frame(self.creating_task_window, background=bg_color)
            extension_sort_frame.pack(anchor='w', padx=20, pady=10, fill='x')
            extension_sort_label: ttk.Label = ttk.Label(extension_sort_frame, text=extension_sort, style='TLabel')
            extension_sort_label.pack(side='left')

            for ext in extensions:
                var: tk.BooleanVar = tk.BooleanVar(value=True)
                checkbox: ttk.Checkbutton = ttk.Checkbutton(extension_sort_frame, text=ext, variable=var, style='TCheckbutton')
                checkbox.pack(side='left', padx=5)
                self.extensions_check_vars[ext] = var
        
        # On déclare quelques variables Tk()
        self.folder_path_var: tk.StringVar = tk.StringVar()
        self.local_only_boolvar: tk.BooleanVar = tk.BooleanVar(value=False)
        self.shuffle_boolvar: tk.BooleanVar = tk.BooleanVar(value=True)

        options_frame: tk.Frame = tk.Frame(self.creating_task_window, background=bg_color)
        options_frame.pack(pady=20, padx=20, fill='x')

        # On déclare les widgets sur la frame options_frame
        folder_button: ttk.Button = ttk.Button(options_frame, text="Select a folder", command=self.select_filesource_folder, style='TButton')
        abort_button = ttk.Button(self.creating_task_window, text="Back", command=self.creating_task_window.destroy, style='TButton')
        confirm_button = ttk.Button(self.creating_task_window, text="Confirm", command=self.confirm_task_creation, style='TButton')
        local_only_checkbox: ttk.Checkbutton = ttk.Checkbutton(options_frame, text="Local Only", variable=self.local_only_boolvar, style='TCheckbutton')
        shuffle_checkbox: ttk.Checkbutton = ttk.Checkbutton(options_frame, text="Shuffle", variable=self.shuffle_boolvar, style='TCheckbutton')
        self.selected_folder_label = ttk.Label(self.creating_task_window, textvariable=self.folder_path_var, style='TLabel')

        # Et enfin on les pack.
        folder_button.pack(side='left')
        local_only_checkbox.pack(side='left', padx=10)
        shuffle_checkbox.pack(side='left', padx=10)
        self.selected_folder_label.pack(pady=10)
        abort_button.pack(pady=20, side='left', padx=20)
        confirm_button.pack(pady=20, side='right', padx=20)

        self.root.wait_window(self.creating_task_window)

    def select_filesource_folder(self) -> None:
        folder_selected = filedialog.askdirectory()
        if folder_selected: self.folder_path_var.set(folder_selected)

    def confirm_task_creation(self) -> None:
        
        # On récupère les extensions séléctionnées et les paramètres
        selected_ext: list[str] = []
        for ext, var in self.extensions_check_vars.items():
            if var.get(): selected_ext.append(ext)

        local_mode: bool = self.local_only_boolvar.get()
        shuffle_mode: bool = self.shuffle_boolvar.get()
        task_path: str = self.folder_path_var.get()

        if not task_path: return
        if not selected_ext: return

        self.creating_task_window.destroy()
        task: SortingTask = SortingTaskDataManager.create_task(
            task_path=task_path,
            selected_ext=selected_ext,
            local_mode=local_mode,
            shuffle_mode=shuffle_mode,
            config_folder=self.supported_extensions_filepath
        )
        self.set_sorting_task(task)

    def on_enter(self, event: tk.Event) -> None:
        self.confirm_task_creation()
    
    def on_escape(self, event: tk.Event) -> None:
        self.creating_task_window.destroy()
    

        



