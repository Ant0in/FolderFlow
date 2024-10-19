

from src.core.assertion_helper import AssertionHelper

from PIL import Image
import cv2
import os
from datetime import datetime




class FileObject:

    # File object meant to be opened by App.
    def __init__(self, fp: str) -> None:
        AssertionHelper.verify_filepath(fp=fp)
        self._fp: str = fp

    def set_new_path(self, new_fp: str) -> None:
        AssertionHelper.verify_filepath(fp=new_fp)
        self._fp = new_fp

    @property
    def path(self) -> str:
        return self._fp
    
    @property
    def dirname(self) -> str:
        return os.path.dirname(self.path)
    
    @property
    def filename(self) -> str:
        return os.path.basename(self.path)
    
    @property
    def extension(self) -> str:
        return os.path.splitext(self.path)[-1]
    
    @property
    def filesize(self) -> int:
        return os.path.getsize(self.path)
    
    @property
    def last_opened(self) -> str:
        return datetime.fromtimestamp(os.path.getatime(self.path)).strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def last_modified(self) -> str:
        return datetime.fromtimestamp(os.path.getmtime(self.path)).strftime("%Y-%m-%d %H:%M:%S")
    
    def get_file_data(self) -> dict[str: str | int]:
        return {
            'path': self.path,
            'name': self.filename,
            'size': self.filesize,
            'last_modified': self.last_modified,
            'last_opened': self.last_opened,
        }

    def close(self) -> None:
        pass



class ImageObject(FileObject):

    def __init__(self, fp: str) -> None:
        super().__init__(fp)

    @property
    def dimension(self) -> tuple:
        try:
            with Image.open(self.path) as img:
                return img.size
        except Exception as img_exception:
            print(f"[W] Impossible de récupérer les dimensions de l'image @ {self.path}. (e: {img_exception})")
            return None

    def get_file_data(self) -> dict:
        data_dict: dict = super().get_file_data()
        data_dict.update({'dimension': self.dimension})
        return data_dict



class VideoObject(FileObject):

    def __init__(self, fp: str) -> None:
        
        super().__init__(fp)
        self.video_cap = None

    def load_video_cap(self) -> None:
        self.video_cap = cv2.VideoCapture(self.path)

    def replay_video(self) -> None:
        if self.video_cap:
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def get_current_frame(self) -> Image:

        # Si le videoCapture n'est pas encore load, on le load.
        if not self.video_cap:
            self.load_video_cap()

        ret, frame = self.video_cap.read()

        # Si la fin de la vidéo a été atteinte, alors ret sera False.
        # On replay alors la vidéo, puis on récupère de nouveau la frame.
        if not ret:
            self.replay_video()
            ret, frame = self.video_cap.read()

        if ret:

            # On transforme la frame en une imagePIL lisible par Tkinter.
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image: Image = Image.fromarray(frame_rgb)
            return pil_image
        
        return None

    def close(self) -> None:
        self.close_video_cap() 

    def close_video_cap(self) -> None:

        if self.video_cap:
            self.video_cap.release()
            self.video_cap = None

    @property
    def dimension(self) -> tuple:
        
        if not self.video_cap:
            self.load_video_cap()

        width: int = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height: int = int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height

    @property
    def duration(self) -> int:

        if not self.video_cap:
            self.load_video_cap()

        fps: float = self.video_cap.get(cv2.CAP_PROP_FPS)
        frame_count: int = self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT)

        return fps if fps == 0 else round(frame_count / fps)

    def get_file_data(self) -> dict:
        
        data_dict: dict = super().get_file_data()
        data_dict.update({
            'dimension': self.dimension,
            'duration': self.duration,
        })
        return data_dict

    
