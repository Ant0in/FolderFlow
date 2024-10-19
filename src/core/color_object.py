

class ColorHelper:

    def __init__(self, color_config: dict) -> None:
        
        self._background1_color: str = color_config['background1_color']
        self._background2_color: str = color_config['background2_color']
        self._header_color: str = color_config['header_color']
        self._footer_color: str = color_config['footer_color']
        self._frame1_color: str = color_config['frame1_color']
        self._frame2_color: str = color_config['frame2_color']
        self._frame3_color: str = color_config['frame3_color']
        self._border_color: str = color_config['border_color']
        self._button1_color: str = color_config['button1_color']
        self._button2_color: str = color_config['button2_color']
        self._text1_color: str = color_config['text1_color']
        self._text2_color: str = color_config['text2_color']
        self._positive_color: str = color_config['positive_color']
        self._negative_color: str = color_config['negative_color']
        self._unusable_button_color: str = color_config['unusable_button_color']
        self._placeholder_color: str = color_config['placeholder_color']
        
    @property
    def background1_color(self) -> str:
        return self._background1_color

    @property
    def background2_color(self) -> str:
        return self._background2_color

    @property
    def header_color(self) -> str:
        return self._header_color

    @property
    def footer_color(self) -> str:
        return self._footer_color

    @property
    def frame1_color(self) -> str:
        return self._frame1_color

    @property
    def frame2_color(self) -> str:
        return self._frame2_color

    @property
    def frame3_color(self) -> str:
        return self._frame3_color

    @property
    def border_color(self) -> str:
        return self._border_color

    @property
    def button1_color(self) -> str:
        return self._button1_color

    @property
    def button2_color(self) -> str:
        return self._button2_color

    @property
    def text1_color(self) -> str:
        return self._text1_color

    @property
    def text2_color(self) -> str:
        return self._text2_color

    @property
    def positive_color(self) -> str:
        return self._positive_color

    @property
    def negative_color(self) -> str:
        return self._negative_color

    @property
    def unusable_button_color(self) -> str:
        return self._unusable_button_color

    @property
    def placeholder_color(self) -> str:
        return self._placeholder_color
    

