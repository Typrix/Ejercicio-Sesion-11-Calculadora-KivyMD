from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

# Tamaño de ventana ideal para vista móvil
Window.size = (360, 640)

class CalculatorScreen(MDScreen):
    """
    Pantalla principal con la Calculadora.
    Estructura:
      - BoxLayout vertical principal.
      - Fila superior (Fila 1 del grid de la imagen): Label del display (3 columnas) + Botón 'C' (1 columna).
      - GridLayout de 4 filas x 4 columnas con el teclado (7,8,9,*, 4,5,6,/, 1,2,3,-, 0,.,=,+).
      - Botón inferior para navegar a la vista secundaria (BoxLayout).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'calculator'
        
        # Layout contenedor principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # --- FILA SUPERIOR (Pantalla + Botón C) ---
        top_box = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)
        
        # Label que actúa como pantalla del resultado
        self.display = MDLabel(
            text="0",
            halign="right",
            valign="middle",
            font_style="H4",
            theme_text_color="Primary",
            size_hint_x=0.75
        )
        self.display.bind(size=self.display.setter('text_size'))
        
        # Botón para limpiar pantalla ('C')
        btn_clear = MDRaisedButton(
            text="C",
            size_hint_x=0.25,
            md_bg_color=(0.85, 0.25, 0.2, 1), # Color rojo destacado
            on_release=self.clear_display
        )
        
        top_box.add_widget(self.display)
        top_box.add_widget(btn_clear)
        main_layout.add_widget(top_box)
        
        # --- TECLADO (GridLayout: 4 filas x 4 columnas) ---
        grid = GridLayout(cols=4, rows=4, spacing=8, size_hint_y=0.7)
        
        # Disposición de botones idéntica a la imagen de referencia
        buttons = [
            '7', '8', '9', '*',
            '4', '5', '6', '/',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        for btn_text in buttons:
            if btn_text == '=':
                btn = MDRaisedButton(
                    text=btn_text,
                    font_size='22sp',
                    on_release=self.calculate_result
                )
            else:
                btn = MDRectangleFlatButton(
                    text=btn_text,
                    font_size='22sp',
                    on_release=self.on_button_press
                )
            grid.add_widget(btn)
            
        main_layout.add_widget(grid)
        
        # --- BOTÓN PARA CAMBIAR A VISTA SECUNDARIA ---
        btn_switch = MDRaisedButton(
            text="Ver Vista Secundaria (BoxLayout)",
            size_hint_y=0.1,
            pos_hint={'center_x': 0.5},
            on_release=self.go_to_secondary
        )
        main_layout.add_widget(btn_switch)
        
        self.add_widget(main_layout)

    def on_button_press(self, instance):
        current = self.display.text
        button_text = instance.text
        
        if current == "0" or current == "Error":
            self.display.text = button_text
        else:
            self.display.text += button_text

    def clear_display(self, instance):
        self.display.text = "0"

    def calculate_result(self, instance):
        try:
            # Evalúa la expresión matemática introducida
            result = eval(self.display.text)
            self.display.text = str(result)
        except Exception:
            self.display.text = "Error"

    def go_to_secondary(self, instance):
        self.manager.current = 'secondary'


class SecondaryScreen(MDScreen):
    """
    Pantalla secundaria para comparar el uso de BoxLayout vertical
    Requerimiento: Título, Campo de texto (MDTextField) y Botón.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'secondary'
        
        # BoxLayout vertical con spacing y padding explícitos
        layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=30
        )
        
        # 1. Título
        title = MDLabel(
            text="Vista Secundaria (BoxLayout)",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=50
        )
        
        # 2. Campo de texto (MDTextField)
        self.input_field = MDTextField(
            hint_text="Escribe un mensaje o nota aquí...",
            mode="rectangle"
        )
        
        # Label para mostrar confirmación al interactuar
        self.info_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Secondary"
        )
        
        # 3. Botón para enviar/procesar
        btn_action = MDRaisedButton(
            text="Procesar Campo",
            pos_hint={'center_x': 0.5},
            on_release=self.process_text
        )
        
        # Botón para regresar a la calculadora
        btn_back = MDRectangleFlatButton(
            text="Volver a Calculadora",
            pos_hint={'center_x': 0.5},
            on_release=self.go_back
        )
        
        # Agregar los widgets al layout
        layout.add_widget(title)
        layout.add_widget(self.input_field)
        layout.add_widget(btn_action)
        layout.add_widget(self.info_label)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)

    def process_text(self, instance):
        if self.input_field.text:
            self.info_label.text = f"Texto capturado: {self.input_field.text}"
        else:
            self.info_label.text = "Por favor ingresa algo en el campo."

    def go_back(self, instance):
        self.manager.current = 'calculator'


class CalculatorApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Gestor de pantallas
        sm = MDScreenManager()
        sm.add_widget(CalculatorScreen())
        sm.add_widget(SecondaryScreen())
        return sm


if __name__ == '__main__':
    CalculatorApp().run()
