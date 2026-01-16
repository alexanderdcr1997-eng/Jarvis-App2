[app]
# Nombre y Dominio
title = JARVIS
package.name = jarvis
package.domain = org.jarvis

# Archivos
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Versión y Requisitos
version = 0.1
requirements = python3,kivy==2.3.0,android,jnius

# Pantalla
orientation = portrait
fullscreen = 0

# Permisos (Voz y Flotante)
android.permissions = INTERNET,RECORD_AUDIO,SYSTEM_ALERT_WINDOW,ACCESS_NETWORK_STATE

# Configuración Android (CRÍTICO)
android.api = 31
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a

# Configuración Buildozer
[buildozer]
log_level = 2
warn_on_root = 1
