

from src.core.file_objects import FileObject, ImageObject, VideoObject
from src.core.sorting_task import SortingTask
from src.core.app_config_object import AppConfigurationObject

import tkinter as tk
from PIL import Image, ImageTk


class FileDisplayer:

    @staticmethod
    def update_display(sorting_task: SortingTask, target_canvas: tk.Canvas, app_config: AppConfigurationObject) -> ImageTk:

        if sorting_task:
            if not sorting_task.is_empty():
                return FileDisplayer.display_file(sorting_task, target_canvas, app_config)

    @staticmethod
    def display_file(sorting_task: SortingTask, target_canvas: tk.Canvas, app_config: AppConfigurationObject) -> ImageTk:
        
        file: FileObject = sorting_task.get_current_file()

        if isinstance(file, ImageObject):
            return FileDisplayer.display_image_file(file, target_canvas, app_config)
        elif isinstance(file, VideoObject):
            return FileDisplayer.display_video_file(file, target_canvas, app_config)
        else: raise NotImplementedError(f'[E] Unknown Filetype {type(file)} for file @ {file.path}.')

    @staticmethod
    def display_image_file(img: ImageObject, target_canvas: tk.Canvas, app_config: AppConfigurationObject) -> ImageTk:
        
        # On refresh le canvas de l'image précédente.
        target_canvas.delete("all")

        pil_image: Image = Image.open(img.path)
        tk_image: ImageTk.PhotoImage = None
        canvas_width: int = target_canvas.winfo_width()
        canvas_height: int = target_canvas.winfo_height()

        # Mode strech fait un resize bête à la taille du canvas.
        if app_config.is_in_stretch_mode():
            pil_image = pil_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)
            target_canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

        # Mode adjust trouve le ratio d'étirement le plus proche du ration du canvas.
        elif app_config.is_in_adjust_mode():

            image_width, image_height = img.dimension
            image_ratio: float = image_width / image_height
            canvas_ratio: float = canvas_width / canvas_height

            if image_ratio > canvas_ratio:
                new_width: int = canvas_width
                new_height: int = round(canvas_width / image_ratio)
            else:
                new_width: int = round(canvas_height * image_ratio)
                new_height: int = canvas_height

            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            x_offset: int = (canvas_width - new_width) // 2
            y_offset: int = (canvas_height - new_height) // 2
            tk_image = ImageTk.PhotoImage(pil_image)
            target_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=tk_image)

        else: pass

        # Pour éviter que l'image se fasse garbage collecter par Tkinter.
        return tk_image

    @staticmethod
    def display_video_file(vid: VideoObject, target_canvas: tk.Canvas, app_config: AppConfigurationObject) -> ImageTk:
        
        # On refresh le canvas de l'image précédente.
        target_canvas.delete("all")

        pil_image: Image = vid.get_current_frame()
        if not pil_image: return

        canvas_width: int = target_canvas.winfo_width()
        canvas_height: int = target_canvas.winfo_height()
        tk_image: ImageTk.PhotoImage = None

        if app_config.is_in_stretch_mode():

            pil_image = pil_image.resize((target_canvas.winfo_width(), target_canvas.winfo_height()), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)
            target_canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

        elif app_config.is_in_adjust_mode():
            
            image_width, image_height = vid.dimension
            image_ratio: float = image_width / image_height
            canvas_ratio: float = canvas_width / canvas_height
            
            if image_ratio > canvas_ratio:
                new_width: int = canvas_width
                new_height: int = round(canvas_width / image_ratio)
            else:
                new_width: int = round(canvas_height * image_ratio)
                new_height: int = canvas_height

            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            x_offset: int = (canvas_width - new_width) // 2
            y_offset: int = (canvas_height - new_height) // 2
            tk_image = ImageTk.PhotoImage(pil_image)
            target_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=tk_image)

        else: pass

        # Pour éviter que l'image se fasse garbage collecter par Tkinter.
        return tk_image
    


