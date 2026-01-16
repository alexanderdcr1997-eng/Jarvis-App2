[app]
title = JARVIS
package.name = jarvis
package.domain = org.jarvis
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,android,jnius

# --- AJUSTES DE PANTALLA ---
orientation = portrait
fullscreen = 0

# --- PERMISOS (Voz y Flotante) ---
android.permissions = INTERNET,RECORD_AUDIO,SYSTEM_ALERT_WINDOW,ACCESS_NETWORK_STATE

# --- CONFIGURACIÓN ANDROID (Lo que fallaba antes) ---
# Aceptamos licencia automáticamente
android.accept_sdk_license = True
# Arquitectura estándar para todos los teléfonos modernos
android.archs = arm64-v8a
# Versiones API automáticas (dejamos que Buildozer decida para evitar errores)
# (No descomentes android.api ni ndk, deja que use los defaults)

[buildozer]
log_level = 2
warn_on_root = 1
