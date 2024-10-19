


from src.core.sorting_task import SortingTask
from src.core.app_config_object import AppConfigurationObject
from src.scripts.name_changer_helper import FilenameManager

import tkinter as tk


class NameChangerGUI:

    def __init__(self, root: tk.Tk, sorting_task: SortingTask, app_config: AppConfigurationObject) -> None:
        
        self.root: tk.Tk = root
        self._sorting_task: SortingTask = sorting_task
        self._app_config: AppConfigurationObject = app_config
        self.has_changed_name: bool = False
        self.init_GUI()

    @property
    def sorting_task(self) -> SortingTask:
        return self._sorting_task
    
    @property
    def app_config(self) -> AppConfigurationObject:
        return self._app_config

    def init_GUI(self) -> None:
        
        if not self.sorting_task: return
        
        bg_color: str = self.app_config.colors.background2_color
        text_color: str = self.app_config.colors.text2_color
        button_color: str = self.app_config.colors.button1_color

        self.name_change_window: tk.Toplevel = tk.Toplevel(self.root)
        self.name_change_window.title("Change File Name")
        self.name_change_window.config(background=bg_color)
        self.name_change_window.grab_set()
        self.name_change_window.bind('<Return>', self.on_enter)
        self.name_change_window.bind('<Escape>', self.on_escape)

        # On déclare les labels puis les boutons, et on pack() enfin.
        self.new_name_label_name_changer: tk.Label = tk.Label(self.name_change_window, text="New Name:", bg=bg_color, fg=text_color)
        self.name_entry: tk.Entry = tk.Entry(self.name_change_window)
        self.confirm_button: tk.Button = tk.Button(self.name_change_window, text="Confirm", command=self.rename_file, bg=button_color, fg=text_color)
        self.cancel_button: tk.Button = tk.Button(self.name_change_window, text="Cancel", command=self.name_change_window.destroy, bg=button_color, fg=text_color)
        self.random_button: tk.Button = tk.Button(self.name_change_window, text="Random", command=self.rename_file_random, bg=button_color, fg=text_color)
        
        self.new_name_label_name_changer.pack(pady=5)
        self.name_entry.pack(pady=5)
        self.confirm_button.pack(side=tk.RIGHT, padx=10, pady=10)
        self.cancel_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.random_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.root.wait_window(self.name_change_window)

    def rename_file(self) -> None:
        new_name: str = self.name_entry.get()
        if not new_name: return
        FilenameManager.rename_file(self.sorting_task, new_name)
        self.has_changed_name = True
        self.name_change_window.destroy()

    def rename_file_random(self) -> None:
        FilenameManager.rename_file_random(self.sorting_task, self.app_config.random_name_length)
        self.has_changed_name = True
        self.name_change_window.destroy()

    def on_enter(self, event: tk.Event) -> None:
        self.rename_file()

    def on_escape(self, event: tk.Event) -> None:
        self.name_change_window.destroy()

