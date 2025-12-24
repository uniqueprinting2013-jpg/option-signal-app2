[app]
title = Option Signal App
package.name = optionsignal
package.domain = org.trader

source.include_exts = py
requirements = python3,kivy,requests,plyer
orientation = portrait

android.permissions = INTERNET,WAKE_LOCK,RECEIVE_BOOT_COMPLETED
android.foreground_service = True
