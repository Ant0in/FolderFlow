

from src.scripts.crawler import Crawler
from src.core.assertion_helper import AssertionHelper


import os
import shutil



class FavoriteManager:

    @staticmethod
    def get_file_list(root_dir: str) -> list[str]:
        return Crawler().crawl_folder(root_dir, local_only=False, shuffle=False, bypass_extension_limitation=True)

    @staticmethod
    def get_favorite_files(root_dir: str, FAVORITE_MARK: str) -> list[str]:
        return [f for f in FavoriteManager.get_file_list(root_dir) if FAVORITE_MARK in f]
    
    @staticmethod
    def copy_favorite_files(files: list[str], path: str, create_subdirs: bool = False) -> None:
        
        AssertionHelper.verify_filepath(path)
        
        if create_subdirs:

            for file in files:
                subdir: str = os.path.basename(os.path.dirname(file))
                fp: str = os.path.join(path, subdir)
                if not os.path.exists(fp): os.mkdir(fp)

                shutil.copy(file, fp)

        else:

            for file in files: shutil.copy(file, path)




    
