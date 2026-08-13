[app]
title = Jarvis Cosmetics AI
package.name = jarviscosmetics
package.domain = org.jarvis.cosmetics
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,mp3,ttf,db,sqlite
version = 2.0.0
requirements = python3,kivy==2.2.1,kivymd==1.1.1,android,pyjnius,speechrecognition,gTTS,pydub,requests,beautifulsoup4,peewee,numpy,regex,python-dateutil
orientation = portrait
fullscreen = 0

android.permissions = INTERNET,RECORD_AUDIO,CALL_PHONE,SEND_SMS,READ_CONTACTS,READ_PHONE_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,BIND_ACCESSIBILITY_SERVICE,SYSTEM_ALERT_WINDOW
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = arm64-v8a

icon.filename = assets/icons/app_icon.png
presplash.filename = assets/icons/app_icon.png

android.release_artifact = apk
android.allow_backup = True
