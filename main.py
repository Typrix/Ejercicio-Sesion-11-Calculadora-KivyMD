from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle


Window.size = (340, 420)

class BorderWidget(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.after:
            Color(0, 0, 0, 1)
            self.line = Line(width=2.5)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.line.rectangle = (self.x, self.y, self.width, self.height)


class FlatButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (1, 1, 1, 1)
        self.color = (0, 0, 0, 1)
        self.font_size = '28sp'
        
        with self.canvas.after:
            Color(0, 0, 0, 1)
            self.line = Line(width=2.5)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.line.rectangle = (self.x, self.y, self.width, self.height)


class CalculatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        main_layout = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=6
        )
        
        top_box = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=6)
        
        display_container = BorderWidget(size_hint_x=0.75, padding=[10, 0, 10, 0])
        self.display = MDLabel(
            text="0",
            halign="right",
            valign="middle",
            font_size="36sp",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
        self.display.bind(size=self.display.setter('text_size'))
        display_container.add_widget(self.display)
        
        btn_clear = FlatButton(
            text="C",
            size_hint_x=0.25,
            on_release=self.clear_display
        )
        
        top_box.add_widget(display_container)
        top_box.add_widget(btn_clear)
        main_layout.add_widget(top_box)
        
        grid = GridLayout(cols=4, rows=4, spacing=6, size_hint_y=0.8)
        
        buttons = [
            '7', '8', '9', '*',
            '4', '5', '6', '/',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        for btn_text in buttons:
            if btn_text == '=':
                btn = FlatButton(text=btn_text, on_release=self.calculate_result)
            else:
                btn = FlatButton(text=btn_text, on_release=self.on_button_press)
            grid.add_widget(btn)
            
        main_layout.add_widget(grid)
        self.add_widget(main_layout)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_button_press(self, instance):
        current = self.display.text
        if current == "0" or current == "Error":
            self.display.text = instance.text
        else:
            self.display.text += instance.text

    def clear_display(self, instance):
        self.display.text = "0"

    def calculate_result(self, instance):
        try:
            result = eval(self.display.text)
            self.display.text = str(result)
        except Exception:
            self.display.text = "Error"


class CalculatorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return CalculatorScreen()


if __name__ == '__main__':
    CalculatorApp().run()
