

from src.gui.subgui.task_creation_gui import TaskCreationGUI
from src.gui.subgui.task_edit_gui import TaskEditGUI
from src.gui.subgui.custom_category_gui import CustomCategoryGUI
from src.gui.subgui.name_changer_gui import NameChangerGUI
from src.gui.subgui.favorite_crawler_gui import FavoriteCrawlerGUI

from src.core.file_objects import FileObject, ImageObject, VideoObject
from src.core.app_config_object import AppConfigurationObject
from src.core.sorting_task import SortingTask
from src.core.assertion_helper import AssertionHelper

from src.scripts.yaml_helper import YAMLSafeHelper
from src.scripts.custom_category_helper import CustomCategoryHelper
from src.scripts.file_display import FileDisplayer
from src.scripts.task_data_manager import SortingTaskDataManager
from src.scripts.name_changer_helper import FilenameManager
from src.scripts.crawler import Crawler
from src.scripts.string_maching_helper import StringMatchHelper


import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import copy
import math
import random
from send2trash import send2trash




class SortingGUI:


    APP_NAME: str = "Ultimate Sorter"
    FAVORITE_MARK: str = '[★]'

    GUI_CONFIG_FILENAME: str = "gui_config.yaml"
    APP_CONFIG_FILENAME: str = "app_config.yaml"
    SUPPORTED_EXTENSIONS_CONFIG_FILENAME: str = "supported.yaml"


    def __init__(self, size: str, config_fp: str) -> None:

        # Public
        self.root: tk.Tk = tk.Tk()
        self.running: bool = False

        # Private
        self._app_configuration: AppConfigurationObject = AppConfigurationObject(os.path.join(config_fp, self.APP_CONFIG_FILENAME))
        self._app_size: str = size
        self._config_fp: str = config_fp
        self._unsaved_modification: bool = False
        self._viewer_mode_var: tk.BooleanVar = tk.BooleanVar()
        self._remove_button_state: tk.BooleanVar = tk.BooleanVar()
        self._sorting_task: SortingTask = None
        self._sorting_task_backup: SortingTask = None
        self._previous_bar_var: str = ""
        self._custom_category_pick: int = 0
        self._current_sorting_categories: dict = dict()

        self.init_app()


    @property
    def app_config(self) -> AppConfigurationObject:
        return self._app_configuration
    
    @property
    def app_size(self) -> str:
        return self._app_size
    
    @property
    def config_folder_path(self) -> str:
        return self._config_fp
    
    @property
    def unsaved_modification(self) -> bool:
        return self._unsaved_modification
    
    @property
    def viewer_mode(self) -> bool:
        return self._viewer_mode_var.get()
    
    @property
    def remove_button_state(self) -> bool:
        return self._remove_button_state.get()
    
    @property
    def search_bar_var(self) -> str:
        return self._search_bar_var.get()

    @property
    def sorting_task(self) -> SortingTask:
        return self._sorting_task

    @property
    def current_sorting_categories(self) -> dict:
        return self._current_sorting_categories
    
    @property
    def custom_category_pick(self) -> int:
        return self._custom_category_pick
    
    @property
    def width(self) -> float:
        return float(self.app_size.split('x')[0])   
    
    @property
    def height(self) -> float:
        return float(self.app_size.split('x')[1])
    
    @property
    def gui_dimension(self) -> dict:
        return self._gui_dim_config

    def set_unsaved_modification(self, boolvar: bool) -> None:
        self._unsaved_modification = boolvar
        self.update_app_status()
    
    def set_viewer_mode_state(self, boolvar: bool) -> None:
        self._viewer_mode_var.set(boolvar)
    
    def set_remove_button_state(self, boolvar: bool) -> None:
        self._remove_button_state.set(boolvar)
    
    def set_search_bar(self, var: str) -> None:
        self._search_bar_var.set(var)

    def set_sorting_task(self, new_sorting_task: SortingTask) -> None:
        self._sorting_task = new_sorting_task

    def is_sorting_task_valid(self) -> bool:
        if self.sorting_task:
            if not self.sorting_task.files.is_empty():
                return True
        return False
 
    def set_custom_category_pick(self, i: int) -> None:
        self._custom_category_pick = i

    @staticmethod
    def config_buttons_color(buttons: list[tk.Button], bg: str, fg: str) -> None:
        for button in buttons: button.config(bg=bg, fg=fg)
    
    @staticmethod
    def clear_frame(frame: tk.Frame) -> None:
        for widget in frame.winfo_children(): widget.destroy()

    # ----- App Init ----- #

    def init_app(self) -> None:

        self.load_gui_dim_config()
        self.config_root()
        self.create_menubar()
        self.create_canvas()
        self.create_buttons()
        self.create_info_labels()

    def load_gui_dim_config(self) -> None:
        gui_config_fp: str = os.path.join(self.config_folder_path, self.GUI_CONFIG_FILENAME)
        self._gui_dim_config: dict = YAMLSafeHelper.safe_load(gui_config_fp)

    def config_root(self) -> None:

        # Configuration de la taille, de la possibilité de resize et d'autres trucs.
        self.root.title(SortingGUI.APP_NAME)
        self.root.geometry(self.app_size)
        self.root.resizable(False, False)
        self.root.config(background=self.app_config.colors.background1_color)

        # Configuration du protocol on-exit, pour permettre de quitter proprement.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configuration des keybinds
        self.root.bind('<Left>', self.on_left_arrow)
        self.root.bind('<Right>', self.on_right_arrow)
        self.root.bind('<Up>', self.on_up_arrow)
        self.root.bind('<Down>', self.on_down_arrow)
        self.root.bind("<Escape>", self.on_escape)
        self.root.bind('<Delete>', self.on_delete)
        self.root.bind('<Return>', self.on_enter)
        self.root.bind('<Control-s>', self.on_ctrl_s)
        self.root.bind('<Control-f>', self.on_ctrl_f)

    def create_menubar(self) -> None:

        # Shortcuts pour les accès aux couleurs en paramètre (+ rapide idk).
        header_color: str = self.app_config.colors.header_color
        bg2_color: str = self.app_config.colors.background2_color
        text1_color: str = self.app_config.colors.text1_color
        text2_color: str = self.app_config.colors.text2_color

        # On crée la MenuBar, puis on la remplie avec les options.
        self.menubar: tk.Menu = tk.Menu(self.root, background=header_color)
        self.root.config(menu=self.menubar)

        # Menu Fichier
        self.file_menu = tk.Menu(self.menubar, tearoff=0, background=header_color)
        self.menubar.add_cascade(label="Task", menu=self.file_menu, foreground=text2_color, background=header_color)
        self.file_menu.add_command(label='New Task', foreground=text1_color, background=bg2_color, command=self.create_task)
        self.file_menu.add_command(label='Edit Task', foreground=text1_color, background=bg2_color, command=self.edit_task)
        self.file_menu.add_separator(background=bg2_color)
        self.file_menu.add_command(label='Load', foreground=text1_color, background=bg2_color, command=self.load_task)
        self.file_menu.add_command(label='Save', foreground=text1_color, background=bg2_color, command=self.save_task)
        self.file_menu.add_command(label='Save as', foreground=text1_color, background=bg2_color, command=self.save_as_task)
        self.file_menu.add_separator(background=bg2_color)
        self.file_menu.add_command(label='Close Task', foreground=text1_color, background=bg2_color, command=self.close_task)

        # Menu Outils
        self.tools_menu = tk.Menu(self.menubar, tearoff=0, background=header_color)
        self.menubar.add_cascade(label="Tools", menu=self.tools_menu, foreground=text2_color, background=header_color)
        self.tools_menu.add_command(label='Auto-generate sorting folders', foreground=text1_color, background=bg2_color, command=self.auto_create_categories)
        self.tools_menu.add_separator(background=bg2_color)
        self.tools_menu.add_command(label='Favorite File Crawler', foreground=text1_color, background=bg2_color, command=self.favorite_file_crawler)
        self.tools_menu.add_separator(background=bg2_color)
        self.tools_menu.add_command(label='Shuffle current Task', foreground=text1_color, background=bg2_color, command=self.shuffle_task)

        # Menu Theme
        self.theme_menu = tk.Menu(self.menubar, tearoff=0, background=header_color)
        self.menubar.add_cascade(label="Themes", menu=self.theme_menu, foreground=text2_color, background=header_color)
        for theme_path in Crawler('.yaml').crawl_folder(os.path.join(self.config_folder_path, 'themes'), True, False):
            self.theme_menu.add_command(
                label=f"{''.join(os.path.splitext(os.path.basename(theme_path))[:-1])}",
                foreground=text1_color,
                background=bg2_color,
                command=lambda theme_path=theme_path: self.load_theme(theme_path)
            )

        # Menu des Paramètres
        self.parameters_menu = tk.Menu(self.menubar, tearoff=0, background=header_color)
        self.menubar.add_cascade(label="Parameters", menu=self.parameters_menu, foreground=text2_color, background=header_color)
        self.parameters_menu.add_checkbutton(label="Viewer Mode", foreground=text1_color, background=bg2_color, selectcolor=text1_color,
                                             variable=self._viewer_mode_var, command=self.viewer_mode_logic)

    def create_canvas(self) -> None:

        # Création des Canvas de la fenêtre principale
        self.create_display_canvas()
        self.create_sorting_util_canvas()
        self.create_sorting_canvas()
        self.create_file_info_canvas()
        self.create_option_canvas()

        # On update rapidement pour mettre à jour les winfo des canvas/frames.
        self.root.update_idletasks()
    
    def create_display_canvas(self) -> None:

        # Le Display Canvas est l'espace utilisé pour afficher les médias.
        # Il se compose d'un grand cadre. Je n'utilise pas de frame car les imageTK
        # fonctionnent avec les canvas et non les frames.

        display_canvas_dim: dict = self.gui_dimension['display_canvas']

        canvas_width: int = int(
            self.width * display_canvas_dim['relative_width'] -
            self.width * self.gui_dimension['right_border_padding'] -
            self.width * self.gui_dimension['left_border_padding']
        )
        
        canvas_height: int = int(
            self.height * display_canvas_dim['relative_height'] -
            self.height * self.gui_dimension['top_border_padding'] -
            self.height * self.gui_dimension['bottom_border_padding']
        )
        
        x_offset: int = int(self.width * display_canvas_dim['x_offset'] + (self.width * self.gui_dimension['left_border_padding']))
        y_offset: int = int(self.height * display_canvas_dim['y_offset'] + (self.height * self.gui_dimension['top_border_padding']))

        self.display_canvas: tk.Canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height,
                                        bg=self.app_config.colors.frame1_color)
        self.display_canvas.place(x=x_offset, y=y_offset)

    def create_sorting_util_canvas(self) -> None:

        # Le Sorting Canvas est l'espace utilisé pour afficher les dossiers de tri personnalisés.
        # Il contient une frame, contenant les boutons d'ajout et de supression des dossiers.

        sorting_utils_canvas_dim: dict = self.gui_dimension['sorting_utils_canvas']

        canvas_width: int = int(
            self.width * sorting_utils_canvas_dim['relative_width'] -
            self.width * self.gui_dimension['right_border_padding'] -
            self.width * self.gui_dimension['left_border_padding']
        )

        canvas_height: int = int(
            self.height * sorting_utils_canvas_dim['relative_height'] -
            self.height * self.gui_dimension['top_border_padding'] -
            self.height * self.gui_dimension['bottom_border_padding']
        )

        x_offset: int = int(self.width * sorting_utils_canvas_dim['x_offset'] + (self.width * self.gui_dimension['left_border_padding']))
        y_offset: int = int(self.height * sorting_utils_canvas_dim['y_offset'] + (self.height * self.gui_dimension['top_border_padding']))

        self.sorting_canvas_utils: tk.Canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg=self.app_config.colors.frame2_color)
        self.sorting_canvas_utils.place(x=x_offset, y=y_offset)
        self.sorting_utilbuttons_frame: tk.Frame = tk.Frame(self.sorting_canvas_utils, background=self.app_config.colors.frame2_color)
        self.sorting_utilbuttons_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def create_sorting_canvas(self) -> None:

        # Le Sorting Canvas est l'espace utilisé pour afficher les dossiers de tri personnalisés.
        # Il contient ces mêmes dossiers personnalisés.

        sorting_canvas_dim: dict = self.gui_dimension['sorting_canvas']
        SCROLLBAR_WIDTH: int = 15

        canvas_width: int = int(
            self.width * sorting_canvas_dim['relative_width'] -
            self.width * self.gui_dimension['right_border_padding'] -
            self.width * self.gui_dimension['left_border_padding']
        )
        
        canvas_height: int = int(
            self.height * sorting_canvas_dim['relative_height'] -
            self.height * self.gui_dimension['top_border_padding'] -
            self.height * self.gui_dimension['bottom_border_padding']
        )
        
        x_offset: int = int(self.width * sorting_canvas_dim['x_offset'] + (self.width * self.gui_dimension['left_border_padding']))
        y_offset: int = int(self.height * sorting_canvas_dim['y_offset'] + (self.height * self.gui_dimension['top_border_padding']))

        self.sorting_canvas: tk.Canvas = tk.Canvas(self.root, width=(canvas_width - SCROLLBAR_WIDTH), height=canvas_height, bg=self.app_config.colors.frame2_color)
        self.sorting_canvas.place(x=x_offset, y=y_offset)

        self.sorting_buttons_frame: tk.Frame = tk.Frame(self.sorting_canvas, background=self.app_config.colors.frame2_color)
        self.sorting_buttons_frame.place(relheight=1.0, relwidth=1.0)

        self.sorting_scrollbar = tk.Scrollbar(self.root, orient="vertical")
        self.sorting_scrollbar.place(x=x_offset*2 + canvas_width - SCROLLBAR_WIDTH, y=y_offset, height=canvas_height)

        self.sorting_canvas_window = self.sorting_canvas.create_window((0, 0), window=self.sorting_buttons_frame, anchor="nw")
        self.sorting_canvas.itemconfig(self.sorting_canvas_window, width=canvas_width)
        self.sorting_buttons_frame.bind("<Configure>", lambda event: self.sorting_canvas.configure(scrollregion=self.sorting_canvas.bbox("all")))

    def create_file_info_canvas(self) -> None:

        # Le File Info Canvas contient les informations importantes à propos des fichiers présentés
        # dans le Display Canvas. Il est composé d'une seule grande frame, dans un canvas.

        info_canvas_dim: dict = self.gui_dimension['info_canvas']

        canvas_width: int = int(
            self.width * info_canvas_dim['relative_width'] -
            self.width * self.gui_dimension['right_border_padding'] -
            self.width * self.gui_dimension['left_border_padding']
        )
        
        canvas_height: int = int(
            self.height * info_canvas_dim['relative_height'] -
            self.height * self.gui_dimension['top_border_padding'] -
            self.height * self.gui_dimension['bottom_border_padding']
        )
        
        x_offset: int = int(self.width * info_canvas_dim['x_offset'] + (self.width * self.gui_dimension['left_border_padding']))
        y_offset: int = int(self.height * info_canvas_dim['y_offset'] + (self.height * self.gui_dimension['top_border_padding']))

        self.info_canvas: tk.Canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height,
                        bg=self.app_config.colors.frame3_color)
        self.info_canvas.place(x=x_offset, y=y_offset)

        # On crée la frame qui contiendra les Labels d'informations.
        self.info_frame: tk.Frame = tk.Frame(self.info_canvas, bg=self.app_config.colors.frame3_color)
        self.info_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def create_option_canvas(self) -> None:

        # Le Option Canvas est le canvas qui contiendra les boutons d'actions directes sur
        # les différents fichiers dans la Task courante.
        # Il est composé d'une seule grande frame, dans un canvas. 

        option_canvas_dim: dict = self.gui_dimension['option_canvas']

        canvas_width: int = int(
            self.width * option_canvas_dim['relative_width'] -
            self.width * self.gui_dimension['right_border_padding'] -
            self.width * self.gui_dimension['left_border_padding']
        )
        
        canvas_height: int = int(
            self.height * option_canvas_dim['relative_height'] -
            self.height * self.gui_dimension['top_border_padding'] -
            self.height * self.gui_dimension['bottom_border_padding']
        )
        
        x_offset: int = int(self.width * option_canvas_dim['x_offset'] + (self.width * self.gui_dimension['left_border_padding']))
        y_offset: int = int(self.height * option_canvas_dim['y_offset'] + (self.height * self.gui_dimension['top_border_padding']))

        self.option_canvas: tk.Canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height,
                                                  bg=self.app_config.colors.frame2_color)
        self.option_canvas.place(x=x_offset, y=y_offset)

        # On crée la frame qui contiendra les boutons d'action.
        self.option_frame: tk.Frame = tk.Frame(self.option_canvas, background=self.app_config.colors.frame2_color)
        self.option_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def create_buttons(self) -> None:
        self.create_option_buttons()
        self.create_sorting_util_buttons()

    def create_option_buttons(self) -> None:
        
        text_color: str = self.app_config.colors.text2_color
        button_color: str = self.app_config.colors.button1_color

        self.previous_file_button: tk.Button = tk.Button(self.option_frame, text="Fichier Précédent ⬅️", bg=button_color,
            foreground=text_color, command=self.previous_task)
        self.next_task_button: tk.Button = tk.Button(self.option_frame, text="Fichier Suivant ➡️", bg=button_color,
            foreground=text_color, command=self.next_task)
        self.favorite_button: tk.Button = tk.Button(self.option_frame, text='Favorite / Unfavorite', bg=button_color,
            foreground=text_color, command=self.toggle_favorite)
        self.resize_button: tk.Button = tk.Button(self.option_frame, text='Étirer / Ajuster', bg=button_color,
            foreground=text_color, command=self.resize_logic)
        self.open_in_folder_button: tk.Button = tk.Button(self.option_frame, text="Ouvrir dans l'explorateur 📁", bg=button_color,
            foreground=text_color, command=self.open_in_folder)
        self.change_name_button: tk.Button = tk.Button(self.option_frame, text='Renommer ✏️', bg=button_color,
            foreground=text_color, command=self.rename)
        self.replay_button: tk.Button = tk.Button(self.option_frame, text='Replay 🔁', bg=button_color,
            foreground=text_color, command=self.replay_video)
        self.trash_button: tk.Button = tk.Button(self.option_frame, text='Trash 🗑️', bg=button_color,
            foreground=text_color, command=self.send_to_trash)

        self.previous_file_button.grid(row=0, column=0, sticky='nsew')
        self.next_task_button.grid(row=0, column=1, sticky='nsew')
        self.resize_button.grid(row=1, column=0, sticky='nsew')
        self.favorite_button.grid(row=1, column=1, sticky='nsew')
        self.open_in_folder_button.grid(row=2, column=0, sticky='nsew')
        self.change_name_button.grid(row=2, column=1, sticky='nsew')
        self.replay_button.grid(row=3, column=0, sticky='nsew')
        self.trash_button.grid(row=3, column=1, sticky='nsew')

        for i in range(4): self.option_frame.grid_rowconfigure(i, weight=1)
        for j in range(2): self.option_frame.grid_columnconfigure(j, weight=1)

    def create_sorting_util_buttons(self) -> None:

        self._search_bar_var: tk.StringVar = tk.StringVar()
        self.remove_button_active: bool = False

        self.add_sorting_button_button: tk.Button = tk.Button(self.sorting_utilbuttons_frame, text="Add Sorting Folder ✔️",
            bg=self.app_config.colors.button1_color, foreground=self.app_config.colors.text2_color, command=self.create_custom_category_logic)
        self.remove_sorting_button_button: tk.Button = tk.Button(self.sorting_utilbuttons_frame, text="Remove Sorting Folder ❌",
            bg=self.app_config.colors.button1_color, foreground=self.app_config.colors.text2_color, command=self.delete_custom_category_logic)
        
        self.search_bar: tk.Entry = tk.Entry(self.sorting_utilbuttons_frame, textvariable=self._search_bar_var, width=40)

        self.add_sorting_button_button.pack(fill=tk.BOTH, expand=True)
        self.remove_sorting_button_button.pack(fill=tk.BOTH, expand=True)
        self.search_bar.pack(fill=tk.BOTH, expand=True)
        
    def create_info_labels(self) -> None:
        
        SortingGUI.clear_frame(self.info_frame)

        vertical_padding: int = math.floor(self.info_frame.winfo_height() / 75)
        horizontal_padding: int = math.floor(self.info_frame.winfo_width() / 500)

        frame_color: str = self.app_config.colors.frame3_color
        text_color: str = self.app_config.colors.text1_color

        self.filename_label: tk.Label = tk.Label(self.info_frame, text="Filename :", bg=frame_color, fg=text_color)
        self.filepath_label: tk.Label = tk.Label(self.info_frame, text="Filepath :", bg=frame_color, fg=text_color)
        self.filesize_label: tk.Label = tk.Label(self.info_frame, text="Filesize (KB) :", bg=frame_color, fg=text_color)
        self.file_dimension_label: tk.Label = tk.Label(self.info_frame, text="Dimension :", bg=frame_color, fg=text_color)
        self.file_duration_label: tk.Label = tk.Label(self.info_frame, text="File duration :", bg=frame_color, fg=text_color)
        self.remaining_files_in_current_task: tk.Label = tk.Label(self.info_frame, text="Remaining Files in current task :", bg=frame_color, fg=text_color)

        self.filename_label.grid(row=0, column=0, padx=horizontal_padding, pady=vertical_padding, sticky=tk.W)
        self.filepath_label.grid(row=1, column=0, padx=horizontal_padding, pady=vertical_padding, sticky=tk.W)
        self.filesize_label.grid(row=2, column=0, padx=horizontal_padding, pady=vertical_padding, sticky=tk.W)
        self.file_dimension_label.grid(row=3, column=0, padx=horizontal_padding, pady=vertical_padding, sticky=tk.W)
        self.file_duration_label.grid(row=4, column=0, padx=horizontal_padding, pady=vertical_padding, sticky=tk.W)
        self.remaining_files_in_current_task.grid(row=5, column=0, padx=horizontal_padding, pady=vertical_padding, sticky=tk.W)

    # ----- Sorting Management ----- #

    def start_sorting_task(self, sortingtask: SortingTask) -> None:
        self.set_sorting_task(sortingtask)
        self.load_custom_categories_buttons()
        self.update_info_frame()
        self.update_app_status()

    def make_sorting_task_backup(self) -> None:
        if not self.sorting_task: return
        self.sorting_task.get_current_file().close()
        self._sorting_task_backup: SortingTask = copy.deepcopy(self.sorting_task)
    
    def load_sorting_task_backup(self) -> None:
        if not self._sorting_task_backup: return
        self.start_sorting_task(self._sorting_task_backup)
        self._sorting_task_backup = None

    def create_custom_category_logic(self) -> None:

        if self.viewer_mode: return
        if not self.is_sorting_task_valid(): return
        
        # Si on veut créer mais que le bouton de supression est actif, on le désactive.
        if self.remove_button_state: self.delete_custom_category_logic()
        cc_gui: CustomCategoryGUI = CustomCategoryGUI(self.root, self.sorting_task, self.app_config)
        if cc_gui.has_created_category:
            self.set_unsaved_modification(True)
            self.load_custom_categories_buttons()

    def delete_custom_category_logic(self) -> None:

        if self.viewer_mode: return
        if not self.sorting_task: return

        # On flip l'état de la valeur booléeenne pour la Tk.Boolvar()
        self.set_remove_button_state(boolvar=(not self.remove_button_state))
        if self.remove_button_state: self.config_buttons_color([self.remove_sorting_button_button],
            bg=self.app_config.colors.unusable_button_color, fg=self.app_config.colors.text2_color)
        else: self.config_buttons_color([self.remove_sorting_button_button],
            bg=self.app_config.colors.button1_color, fg=self.app_config.colors.text2_color)

    def sorting_button_logic(self, cc: dict) -> None:
        
        if self.viewer_mode: return
        if not self.is_sorting_task_valid(): return
        
        # Logique de supression ;
        if self.remove_button_state:
            CustomCategoryHelper.delete_custom_category(self.sorting_task, cc)
            self.set_unsaved_modification(True)
            
            self.delete_custom_category_logic()
            self.load_custom_categories_buttons()

        # Logique de redirection ;
        else:
            status: bool = CustomCategoryHelper.move_file_into_category(self.sorting_task, cc)
            if status: self.next_task()

        self.set_search_bar('')

    def load_custom_categories_buttons(self) -> None:
 
        # On clear la frame avant de replacer les catégories présentes dans la SortingTask.

        # print(self.sorting_canvas.winfo_width(), self.sorting_buttons_frame.winfo_width())

        self.clear_frame(self.sorting_buttons_frame)
        self.current_sorting_categories.clear()

        if not self.sorting_task: return

        text_color: str = self.app_config.colors.text1_color
        entry: str = self.search_bar_var
        button_height: int = 30
        
        i: int = 0

        for custom_category in self.sorting_task.get_custom_categories(sort_by_name=True):
            
            # Si la catégorie ne match pas avec le champ de recherche, alors on peut simplement le skip
            if not StringMatchHelper.string_match(entry, custom_category['name']): continue

            if i == self.custom_category_pick:
                button_color: str = self.app_config.colors.button1_color
                text_color: str = self.app_config.colors.text2_color
            else:
                button_color:str = self.app_config.colors.button2_color
                text_color: str = self.app_config.colors.text1_color

            cc_button: tk.Button = tk.Button(self.sorting_buttons_frame, text=f"{custom_category['name']}",
                    bg=button_color,
                    foreground=text_color,
                    command=lambda custom_category=custom_category: self.sorting_button_logic(custom_category))
            
            cc_button.place(relwidth=1, rely=0, y=(i * button_height), height=button_height)
            
            self.current_sorting_categories[i] = custom_category
            self.current_sorting_categories[i].update({'button_ref': cc_button})

            i += 1

        # On redimensionne rapidement de la frame et on désactive le scroll si il n'est pas nécessaire
        total_height = i * button_height
        self.toggle_sorting_scroll((total_height >= self.sorting_buttons_frame.winfo_height()))
        self.sorting_buttons_frame.config(height=total_height)

    # ----- Task Options (Menubar) ----- #

    def create_task(self) -> None:

        if self.viewer_mode: return
        
        task_gui: TaskCreationGUI = TaskCreationGUI(self.root, self.app_config,
                                os.path.join(self.config_folder_path, self.SUPPORTED_EXTENSIONS_CONFIG_FILENAME))
        created_task: SortingTask = task_gui.sorting_task

        if created_task:
            self.start_sorting_task(created_task)
            self.set_unsaved_modification(True)

    def edit_task(self) -> None:
        
        if not self.is_sorting_task_valid(): return
        if self.viewer_mode: return

        gui: TaskEditGUI = TaskEditGUI(root=self.root, app_config=self.app_config, sorting_task=self.sorting_task)

    def load_task(self) -> None:

        if self.viewer_mode: return
        
        new_task: SortingTask = SortingTaskDataManager.load_task(os.path.join(self.config_folder_path, self.SUPPORTED_EXTENSIONS_CONFIG_FILENAME))
        if new_task:
            self.set_unsaved_modification(False)
            self.start_sorting_task(new_task)

    def save_task(self) -> None:

        if not self.sorting_task: return
        if self.viewer_mode: return
        if SortingTaskDataManager.save_task(self.sorting_task, self.sorting_task.path):
            self.set_unsaved_modification(False)

    def save_as_task(self) -> None:
        if not self.sorting_task: return
        if self.viewer_mode: return
        if SortingTaskDataManager.save_as_task(self.sorting_task):
            self.set_unsaved_modification(False)

    def close_task(self) -> None:

        if not self.sorting_task: return
        if self.viewer_mode: return
        # Pas besoin de del ici, puisque Python est garbage collecté.
        self.start_sorting_task(None)
        self.set_unsaved_modification(False)

    # ----- Sorting Options Management ----- #

    def next_task(self) -> None:

        if not self.sorting_task: return

        # On dequeue le fichier top puis on le close.
        p: FileObject = self.sorting_task.file_dequeue()
        if not p: return
        p.close()
        
        # En viewer mode on ne demande pas de sauvegarder.
        if not self.viewer_mode: self.set_unsaved_modification(True)
        self.update_info_frame()

    def previous_task(self) -> None:

        if not self.sorting_task: return

        # On récupère le fichier top juste pour le fermer.
        c: FileObject = self.sorting_task.get_current_file()
        if c: c.close()
        
        p: FileObject = self.sorting_task.get_most_recent_reviewed_file()
        if p: self.set_unsaved_modification(True)

        self.sorting_task.restore_previous_reviewed_file()
        self.update_info_frame()

    def resize_logic(self) -> None:
        if not self.app_config: return
        self.app_config.switch_resize_mode()
        self.app_config.save_config()
        self.update_app_status()

    def open_in_folder(self) -> None:

        if not self.is_sorting_task_valid(): return

        AssertionHelper.verify_filepath(self.sorting_task.get_current_file().path)
        subprocess.Popen(f"explorer /select,{os.path.normpath(self.sorting_task.get_current_file().path)}")

    def replay_video(self) -> None:

        if not self.sorting_task: return

        current: FileObject = self.sorting_task.get_current_file()
        if isinstance(current, VideoObject): current.replay_video()

    def send_to_trash(self) -> None:

        if self.viewer_mode: return
        if not self.is_sorting_task_valid(): return
        
        self.next_task()
        p: FileObject = self.sorting_task.get_most_recent_reviewed_file()
        send2trash(os.path.normpath(p.path))
        self.sorting_task.reviewed_files.remove(p)

        self.set_unsaved_modification(True)
        self.update_info_frame()

    def rename(self) -> None:

        if self.viewer_mode: return
        if not self.is_sorting_task_valid(): return

        rename_gui: NameChangerGUI = NameChangerGUI(self.root, self.sorting_task, self.app_config)
        if rename_gui.has_changed_name: self.set_unsaved_modification(True)

        self.update_info_frame()
    
    def toggle_favorite(self) -> None:

        if self.viewer_mode: return
        if not self.is_sorting_task_valid(): return

        current: FileObject = self.sorting_task.get_current_file()
        current.close()
        no_ext_filename: str = '.'.join(os.path.splitext(current.filename)[:-1:])

        if self.FAVORITE_MARK in current.filename:
            FilenameManager.rename_file(self.sorting_task, no_ext_filename.replace(self.FAVORITE_MARK, ''))
        else:
            FilenameManager.rename_file(self.sorting_task, (self.FAVORITE_MARK + no_ext_filename))
        
        self.set_unsaved_modification(True)
        self.update_info_frame()

    # ----- Tools Options Management ----- #

    def auto_create_categories(self) -> None:

        if not self.is_sorting_task_valid(): return
        if self.viewer_mode: return

        status: bool = CustomCategoryHelper.add_custom_categories_from_dir(self.sorting_task)
        if status:
            self.set_unsaved_modification(True)
            self.load_custom_categories_buttons()

    def favorite_file_crawler(self) -> None:
        FavoriteCrawlerGUI(root=self.root, app_config=self.app_config, favorite_mark=self.FAVORITE_MARK)

    def shuffle_task(self) -> None:
        
        if not self.is_sorting_task_valid(): return
        if self.viewer_mode: return

        c: FileObject = self.sorting_task.get_current_file()
        if c: c.close()

        random.shuffle(self.sorting_task.files.values)
        self.set_unsaved_modification(True)
        self.update_info_frame()

    # ----- Parameters (Menubar) ----- #

    def viewer_mode_logic(self) -> None:
            
        if self.viewer_mode:
            self.make_sorting_task_backup()
            self.sorting_task.clear_custom_categories()
            button_color: str = self.app_config.colors.unusable_button_color

        else:
            self.load_sorting_task_backup()
            button_color: str = self.app_config.colors.button1_color

        self.config_buttons_color(
            [
                self.change_name_button, self.favorite_button, self.trash_button,
                self.add_sorting_button_button, self.remove_sorting_button_button
            ],
            bg=button_color, fg=self.app_config.colors.text2_color
        )

        self.load_custom_categories_buttons()
        self.update_info_frame()
        self.update_app_status()

    def load_theme(self, theme_path: str) -> None:
        self.app_config.load_theme(theme_path)
        self.update_all_graphics()

    # ----- Shortcuts Logic ----- #

    def on_left_arrow(self, event: tk.Event) -> None:
        self.previous_task()

    def on_right_arrow(self, event: tk.Event) -> None:
        self.next_task()

    def on_up_arrow(self, event: tk.Event) -> None:
        
        if self.viewer_mode: return
        if not self.current_sorting_categories: return

        if self.custom_category_pick == 0: new_pick = max(self.current_sorting_categories)
        else: new_pick: int = self.custom_category_pick - 1

        data: dict = self.current_sorting_categories.get(new_pick)

        if data:
            self.current_sorting_categories.get(self.custom_category_pick)['button_ref'].config(bg=self.app_config.colors.button2_color, fg=self.app_config.colors.text1_color)
            self.set_custom_category_pick(new_pick)
            self.current_sorting_categories.get(self.custom_category_pick)['button_ref'].config(bg=self.app_config.colors.button1_color, fg=self.app_config.colors.text2_color)

    def on_down_arrow(self, event: tk.Event) -> None:
        
        if self.viewer_mode: return
        if not self.current_sorting_categories: return
        
        # Gestion du cas ou on veut remonter en haut en descendant depuis le dernier
        if self.custom_category_pick == max(self.current_sorting_categories): new_pick = 0
        else: new_pick: int = self.custom_category_pick + 1

        data: dict = self.current_sorting_categories.get(new_pick)

        if data:
            self.current_sorting_categories.get(self.custom_category_pick)['button_ref'].config(bg=self.app_config.colors.button2_color, fg=self.app_config.colors.text1_color)
            self.set_custom_category_pick(new_pick)
            self.current_sorting_categories.get(self.custom_category_pick)['button_ref'].config(bg=self.app_config.colors.button1_color, fg=self.app_config.colors.text2_color)

    def on_enter(self, event: tk.Event) -> None:

        cc_dict: dict = self.current_sorting_categories.get(self.custom_category_pick)
        # print(cc_dict)
        self.sorting_button_logic(cc_dict)

    def on_mouse_wheel(self, event: tk.Event) -> None:
        
        UNITS: float = 1

        if event.delta > 0: self.sorting_canvas.yview_scroll(-UNITS, "units")
        elif event.delta < 0: self.sorting_canvas.yview_scroll(UNITS, "units")
        else: pass

    def on_escape(self, event: tk.Event) -> None:
        self.root.iconify()

    def on_delete(self, event: tk.Event) -> None:
        self.send_to_trash()

    def on_ctrl_s(self, event: tk.Event) -> None:
        self.save_task()

    def on_ctrl_f(self, event: tk.Event) -> None:
        self.toggle_favorite()

    # ----- App Logic (Update / Loop) ----- #

    def toggle_sorting_scroll(self, toggle: bool) -> None:

        if toggle:
            self.sorting_canvas.configure(yscrollcommand=self.sorting_scrollbar.set)
            self.sorting_scrollbar.config(command=self.sorting_canvas.yview)
            self.root.bind("<MouseWheel>", self.on_mouse_wheel)
        else:
            self.sorting_canvas.yview_moveto(0.0)
            self.sorting_canvas.configure(yscrollcommand=None)
            self.sorting_scrollbar.config(command=None)
            self.root.unbind("<MouseWheel>")

    def detect_entry(self) -> None:
        
        if self.search_bar_var != self._previous_bar_var:
            self.set_custom_category_pick(0)
            self.load_custom_categories_buttons()

        self._previous_bar_var = self.search_bar_var

    def update_app(self) -> None:
        
        # Update le fichier displayed.
        self.current_image = FileDisplayer.update_display(self.sorting_task, self.display_canvas, self.app_config)
        self.detect_entry()
        self.root.update()  # Applique les updates à la fenêtre TK.

    def update_info_frame(self) -> None:
        
        info_frame_color: str = self.app_config.colors.frame3_color
        text_color: str = self.app_config.colors.text1_color
        
        # On réutilise le template de base pour les cas de base c:
        if not self.is_sorting_task_valid():
            self.create_info_labels()
            return

        current_file_data: dict = self.sorting_task.get_current_file().get_file_data()
        self.filename_label.config(text=f"Filename : {current_file_data.get('name', 'N/A')}", bg=info_frame_color, fg=text_color)
        self.filepath_label.config(text=f"Filepath : {current_file_data.get('path', 'N/A')}", bg=info_frame_color, fg=text_color)
        self.filesize_label.config(text=f"Filesize (KB) : {round(current_file_data.get('size', 0) / 1000, 2)} KB", bg=info_frame_color, fg=text_color)
        imgx, imgy = current_file_data.get('dimension', (0, 0))
        self.file_dimension_label.config(text=f"Dimension : {imgx}x{imgy}", bg=info_frame_color, fg=text_color)
        self.file_duration_label.config(text=f"File duration : {current_file_data.get('duration', 'N/A')} sec", bg=info_frame_color, fg=text_color)

        if self.viewer_mode:
            self.remaining_files_in_current_task.config(text=f"", bg=info_frame_color, fg=text_color) 
        else:
            self.remaining_files_in_current_task.config(text=f"Remaining Files in current task : {self.sorting_task.size} ({round(((self.sorting_task.init_file_count - self.sorting_task.size) / self.sorting_task.init_file_count) * 100, 2)}%)", bg=info_frame_color, fg=text_color)
            
    def update_app_status(self) -> None:

        # Quelques updates contextuelles devant être effectuées dans des cas particuliers.

        # Nom de l'application.
        if self.viewer_mode:
            self.root.title(f'{self.APP_NAME} - Viewer Mode (Safe Mode)')
        else:
            if self.unsaved_modification: self.root.title(f'{self.APP_NAME} ***')
            else: self.root.title(self.APP_NAME)

        # Texte sur le bouton de resize
        if self.app_config.is_in_adjust_mode(): self.resize_button.config(text='Stretch ↔️')
        else: self.resize_button.config(text='Adjust ⬜')

        # Rapide check qu'une task est en cours
        if self.viewer_mode: return
        if not self.is_sorting_task_valid(): return
        
        # Texte sur le bouton de favori
        if self.FAVORITE_MARK in self.sorting_task.get_current_file().filename:
            self.favorite_button.config(text='Unfavorite 💔', bg=self.app_config.colors.negative_color, fg=self.app_config.colors.text2_color)
        else:
            self.favorite_button.config(text='Favorite ★', bg=self.app_config.colors.positive_color, fg=self.app_config.colors.text2_color)

    def update_all_graphics(self) -> None:
        
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_menubar()
        self.create_canvas()
        self.create_buttons()
        self.create_info_labels()
        self.root.geometry(self.app_size)
        self.root.config(background=self.app_config.colors.background1_color)
        self.load_custom_categories_buttons()

        self.update_app_status()
        self.update_info_frame()

    def on_closing(self) -> None:

        # On ferme le viewer en premier lieu.
        if self.viewer_mode: self.viewer_mode_logic()

        if self.unsaved_modification:
            
            response: bool = messagebox.askyesnocancel(
                title="Warning",
                message="All data that isn't saved will be ereased forever. Do you want to save before quitting ?"
            )

            if response is not None:
                if response: self.save_task()
                self.quit_app()

        else: self.quit_app()

    def quit_app(self) -> None:
        self.running = False
        self.root.destroy()

    def run(self) -> None:

        self.running = True
        self.update_app_status()

        while self.running:
            self.update_app()
            

