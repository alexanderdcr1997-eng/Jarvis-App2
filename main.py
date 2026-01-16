import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.window import Window

# Configuración visual (Negro Tech)
Window.clearcolor = (0.05, 0.05, 0.05, 1)

class JarvisMobile(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # 1. Estado de Jarvis
        self.lbl_status = Label(
            text="JARVIS SYSTEM\nEn espera...",
            color=(0, 1, 1, 1), # Cyan
            font_size='22sp',
            halign='center'
        )
        self.add_widget(self.lbl_status)

        # 2. Botón de Voz Principal
        self.btn_listen = Button(
            text="🎙️ ACTIVAR COMANDO",
            size_hint=(1, 0.25),
            background_color=(0, 0.5, 0.5, 1),
            font_size='20sp'
        )
        self.btn_listen.bind(on_press=self.activar_microfono)
        self.add_widget(self.btn_listen)

        # 3. Botón de Permisos Avanzados (Flotante)
        self.btn_float = Button(
            text="⚙️ Habilitar Ventana Flotante",
            size_hint=(1, 0.15),
            background_color=(0.2, 0.2, 0.2, 1)
        )
        self.btn_float.bind(on_press=self.pedir_permiso_flotante)
        self.add_widget(self.btn_float)

        # Iniciar permisos básicos al abrir
        if platform == 'android':
            self.pedir_permisos_basicos()
            # Enlazar resultado de voz
            from android import activity
            activity.bind(on_activity_result=self.on_activity_result)

    def pedir_permisos_basicos(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.RECORD_AUDIO])
        except:
            pass

    def pedir_permiso_flotante(self, instance):
        # Este permiso es especial, hay que ir a Ajustes
        self.lbl_status.text = "Abriendo ajustes de superposición..."
        if platform == 'android':
            try:
                from jnius import autoclass
                Settings = autoclass('android.provider.Settings')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                # Intent para ir directo al menu "Mostrar sobre otras apps"
                intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
                # Opcional: intent.setData(Uri.parse("package:" + PythonActivity.mActivity.getPackageName()))
                
                currentActivity = PythonActivity.mActivity
                currentActivity.startActivity(intent)
            except Exception as e:
                self.lbl_status.text = f"Error: {e}"

    def activar_microfono(self, instance):
        if platform == 'android':
            try:
                from jnius import autoclass
                RecognizerIntent = autoclass('android.speech.RecognizerIntent')
                Intent = autoclass('android.content.Intent')
                
                intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, 'es-ES')
                intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "JARVIS te escucha...")
                
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                PythonActivity.mActivity.startActivityForResult(intent, 100)
            except Exception as e:
                self.lbl_status.text = f"Error Voz: {e}"
        else:
            self.lbl_status.text = "Modo PC: Simulación de voz..."

    def on_activity_result(self, request_code, result_code, intent):
        if request_code == 100 and result_code == -1:
            matches = intent.getStringArrayListExtra('android.speech.extra.RESULTS')
            if matches and matches.size() > 0:
                comando = matches.get(0).lower()
                self.lbl_status.text = f"Procesando: {comando}"
                self.ejecutar_comando(comando)
        return True

    def ejecutar_comando(self, comando):
        apps = {
            "whatsapp": "com.whatsapp",
            "youtube": "com.google.android.youtube",
            "facebook": "com.facebook.katana",
            "spotify": "com.spotify.music",
            "instagram": "com.instagram.android",
            "tiktok": "com.zhiliaoapp.musically",
            "mapas": "com.google.android.apps.maps"
        }
        
        encontrado = False
        for key, package in apps.items():
            if key in comando:
                self.abrir_app(package, key)
                encontrado = True
                break
        
        if not encontrado:
            self.lbl_status.text = "No entendí qué abrir."

    def abrir_app(self, package_name, app_name):
        self.lbl_status.text = f"Abriendo {app_name.upper()}..."
        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                PackageManager = PythonActivity.mActivity.getPackageManager()
                
                intent = PackageManager.getLaunchIntentForPackage(package_name)
                if intent:
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    PythonActivity.mActivity.startActivity(intent)
                else:
                    self.lbl_status.text = f"{app_name} no está instalada."
            except Exception as e:
                self.lbl_status.text = "Error al lanzar app."

class JarvisApp(App):
    def build(self):
        return JarvisMobile()

if __name__ == '__main__':
    JarvisApp().run()