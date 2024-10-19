
from src.scripts.favorite_manager import FavoriteManager
from src.core.app_config_object import AppConfigurationObject
from src.core.assertion_helper import AssertionHelper

import tkinter as tk
from tkinter import filedialog
import os



class FavoriteCrawlerGUI:

    """
    A graphical user interface for selecting source and destination directories to 
    copy favorite files marked with a specific symbol.

    Attributes:
    - root (tk.Tk): The main application window.
    - _app_config (AppConfigurationObject): The application configuration object.
    - _target_directory (tk.StringVar): The source directory for favorite files.
    - _direction_folder (tk.StringVar): The destination directory for copying files.
    - _create_subdir (tk.BooleanVar): A flag indicating whether to create subdirectories.
    - _favorite_mark (str): The marker used to identify favorite files.

    Methods:
    - __init__(root: tk.Tk, app_config: AppConfigurationObject, favorite_mark: str = '[★]'): Initializes the GUI and sets default values.
    - init_GUI() -> None: Initializes and configures the GUI components for the favorite file crawler.
    - ask_target_directory() -> None: Prompts the user to select a source directory.
    - ask_destination_directory() -> None: Prompts the user to select a destination directory.
    - on_quit() -> None: Closes the favorite crawler window.
    - on_confirm() -> None: Confirms the selected directories, verifies them, and copies favorite files.
    - on_enter(event: tk.Event) -> None: Handles the Enter key event to confirm selections.
    - on_escape(event: tk.Event) -> None: Handles the Escape key event to close the window.

    Properties:
    - app_config: Returns the application configuration object.
    - target_directory: Returns the selected source directory.
    - direction_folder: Returns the selected destination directory.
    - create_subdir: Returns whether to create subdirectories.
    - favorite_mark: Returns the favorite file marker.
    - set_target_directory(new_dir: str) -> None: Sets the target directory for favorite files.
    - set_direction_directory(new_dir: str) -> None: Sets the destination directory for copied files.
    - set_create_subdir(boolvar: bool) -> None: Sets the flag for creating subdirectories.
    """

    def __init__(self, root: tk.Tk, app_config: AppConfigurationObject, favorite_mark: str = '[★]') -> None:
        
        self.root: tk.Tk = root
        self._app_config: AppConfigurationObject = app_config

        self._target_directory = tk.StringVar(value=None)
        self._direction_folder: tk.StringVar = tk.StringVar(value=None)
        self._create_subdir: tk.BooleanVar = tk.BooleanVar(value=False)
        self._favorite_mark: str = favorite_mark

        self.init_GUI()

    @property
    def app_config(self) -> AppConfigurationObject:
        return self._app_config

    @property
    def target_directory(self) -> str:
        return self._target_directory.get()
    
    @property
    def direction_folder(self) -> str:
        return self._direction_folder.get()

    @property
    def create_subdir(self) -> bool:
        return self._create_subdir.get()

    @property
    def favorite_mark(self) -> str:
        return self._favorite_mark

    def set_target_directory(self, new_dir: str) -> None:
        self._target_directory.set(new_dir)

    def set_direction_directory(self, new_dir: str) -> None:
        self._direction_folder.set(new_dir)

    def set_create_subdir(self, boolvar: bool) -> None:
        self._create_subdir.set(boolvar)

    def init_GUI(self) -> None:
        
        bg_color: str = self.app_config.colors.background2_color
        button_color: str = self.app_config.colors.button1_color
        text_color: str = self.app_config.colors.text2_color

        self.favorite_crawler_window: tk.Toplevel = tk.Toplevel(self.root)
        self.favorite_crawler_window.title("Favorite File Crawler")
        self.favorite_crawler_window.config(background=bg_color)
        self.favorite_crawler_window.grab_set()
        self.favorite_crawler_window.bind('<Return>', self.on_enter)
        self.favorite_crawler_window.bind('<Escape>', self.on_escape)

        frame1 = tk.Frame(self.favorite_crawler_window, background=bg_color)
        frame2 = tk.Frame(self.favorite_crawler_window, background=bg_color)
        frame3 = tk.Frame(self.favorite_crawler_window, background=bg_color)
        frame4 = tk.Frame(self.favorite_crawler_window, background=bg_color)
        frame1.pack(pady=5)
        frame2.pack(pady=5)
        frame3.pack(pady=5)
        frame4.pack(pady=20)
        
        target_button = tk.Button(frame1, text="Select Source Folder", background=button_color, foreground=text_color, command=self.ask_target_directory)
        destination_button = tk.Button(frame2, text="Select Destination Folder", background=button_color, foreground=text_color, command=self.ask_destination_directory)
        self.target_folder_label = tk.Label(frame1, textvariable=self._target_directory, background=bg_color, foreground=text_color)
        self.destination_folder_label = tk.Label(frame2, textvariable=self._direction_folder, background=bg_color, foreground=text_color)
        target_button.pack(side=tk.LEFT, padx=5)
        destination_button.pack(side=tk.LEFT, padx=5)
        self.target_folder_label.pack(side=tk.LEFT, padx=5)
        self.destination_folder_label.pack(side=tk.LEFT, padx=5)

        checkbutton = tk.Checkbutton(frame3, text="Create subdir", variable=self._create_subdir, background=bg_color, foreground='#000000')
        checkbutton.pack(side=tk.LEFT, padx=5)
           
        back_button = tk.Button(frame4, text="Back", background=button_color, foreground=text_color, command=self.on_quit)
        confirm_button = tk.Button(frame4, text="Confirm", background=button_color, foreground=text_color, command=self.on_confirm)
        back_button.pack(side=tk.LEFT, padx=20)
        confirm_button.pack(side=tk.RIGHT, padx=20)

        self.root.wait_window(self.favorite_crawler_window)

    def ask_target_directory(self) -> None:
        target_dir_path: str = filedialog.askdirectory(title="Select a directory")
        if not os.path.isdir(target_dir_path): return
        self.set_target_directory(target_dir_path)

    def ask_destination_directory(self) -> None:
        dest_dir_path: str = filedialog.askdirectory(title="Select a directory")
        if not os.path.isdir(dest_dir_path): return
        self.set_direction_directory(dest_dir_path)

    def on_quit(self) -> None:
        self.favorite_crawler_window.destroy()

    def on_confirm(self) -> None:
        
        if not (self.target_directory and self.direction_folder): return
        AssertionHelper.verify_filepath(self.target_directory)
        AssertionHelper.verify_filepath(self.direction_folder)
        
        fav_files: list[str] = FavoriteManager.get_favorite_files(self.target_directory, self.favorite_mark)
        FavoriteManager.copy_favorite_files(files=fav_files, path=self.direction_folder, create_subdirs=self.create_subdir)

        self.on_quit()

    def on_enter(self, event: tk.Event) -> None:
        self.on_confirm()
    
    def on_escape(self, event: tk.Event) -> None:
        self.on_quit()
