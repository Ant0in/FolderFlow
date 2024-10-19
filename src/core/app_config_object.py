

from src.core.assertion_helper import AssertionHelper
from src.core.color_object import ColorHelper
from src.scripts.yaml_helper import YAMLSafeHelper



class AppConfigurationObject:

    """
    AppConfigurationObject is a class responsible for managing the application's configuration settings,
    which are loaded from a YAML file. It handles parameters related to resizing modes and color schemes, 
    ensuring the correct format and values are applied.

    Key functionalities:
    - Loads and validates the application configuration from the specified YAML file.
    - Provides access to various configuration properties such as color schemes and resize modes.
    - Allows switching between different resize modes (adjust and stretch).
    - Saves updated configuration back to the YAML file.
    - Supports loading and applying new color themes from external YAML files.

    Attributes:
    - config_file_path (str): The file path of the configuration file.
    - random_name_length (int): The length of the random name to be generated.
    - colors (ColorHelper): The color settings for the application.
    - resize_mode (int): The current resize mode (0 for adjust, 1 for stretch).
    """
    
    def __init__(self, config_fp: str) -> None:
        
        AssertionHelper.verify_file_extension(config_fp, '.yaml')
        self._config_fp: str = config_fp
        self.load_config()

    def load_config(self) -> None:
        
        # On load le fichier de config yaml pour récupérer les paramètres.
        app_config: dict = YAMLSafeHelper.safe_load(self.config_file_path)
                
        if app_config['resize_mode'] == 'adjust': self._resize_mode: int = 0
        elif app_config['resize_mode'] == 'stretch': self._resize_mode: int = 1
        else: raise ValueError(f'[E] Mode de configuration inconnu pour le resize (={self._resize_mode}).')

        self._color_config: ColorHelper = ColorHelper(app_config)
        self._random_name_length: int = app_config['random_name_length']
        
    @property
    def config_file_path(self) -> str:
        return self._config_fp

    @property
    def random_name_length(self) -> int:
        return self._random_name_length

    @property
    def colors(self) -> ColorHelper:
        return self._color_config

    @property
    def resize_mode(self) -> int:
        return self._resize_mode
 
    def is_in_adjust_mode(self) -> bool:
        return self.resize_mode == 0

    def is_in_stretch_mode(self) -> bool:
        return self.resize_mode == 1
     
    def switch_resize_mode(self) -> None:

        if self.is_in_adjust_mode(): self._resize_mode = 1
        elif self.is_in_stretch_mode(): self._resize_mode = 0
        else: raise ValueError(f'[E] Mode de resize inconnu (={self._resize_mode}).')

    def save_config(self) -> None:

        new_data: dict = {

            'resize_mode': 'adjust' if self.is_in_adjust_mode() else 'stretch',
            'random_name_length': self.random_name_length,

            'background1_color': self.colors.background1_color,
            'background2_color': self.colors.background2_color,
            'header_color': self.colors.header_color,
            'footer_color': self.colors.footer_color,
            'frame1_color': self.colors.frame1_color,
            'frame2_color': self.colors.frame2_color,
            'frame3_color': self.colors.frame3_color,
            'border_color': self.colors.border_color,
            'button1_color': self.colors.button1_color,
            'button2_color': self.colors.button2_color,
            'text1_color': self.colors.text1_color,
            'text2_color': self.colors.text2_color,
            'positive_color': self.colors.positive_color,
            'negative_color': self.colors.negative_color,
            'unusable_button_color': self.colors.unusable_button_color,
            'placeholder_color': self.colors.placeholder_color,
        }

        YAMLSafeHelper.safe_dump(self.config_file_path, new_data)

    def load_theme(self, theme_path: str) -> None:

        AssertionHelper.verify_file_extension(theme_path, '.yaml')
        new_colors: dict = YAMLSafeHelper.safe_load(theme_path)
        self._color_config = ColorHelper(new_colors)
        self.save_config()


