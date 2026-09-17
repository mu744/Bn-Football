"""
BN-Football
Configuration Android / APK

Ce fichier centralise les informations qui seront
utilisées lors de la génération de l'application.
"""

APP_NAME = "BN-Football"

PACKAGE_NAME = "com.bndigital.football"

VERSION = "1.0.0"

VERSION_CODE = 1

ORIENTATION = "landscape"

MIN_ANDROID_VERSION = 26

TARGET_ANDROID_VERSION = 35

SUPPORTED_INPUTS = [
    "touch",
    "keyboard",
    "gamepad"
]

GRAPHICS_MODES = [
    "economy",
    "standard",
    "high",
    "3d"
]

DEFAULT_GRAPHICS_MODE = "standard"

DEFAULT_FPS = 60

SAVE_DIRECTORY = "saves"

ASSETS_DIRECTORY = "assets"

GAME_DIRECTORY = "BN-Football"


def get_app_info():

    return {
        "name": APP_NAME,
        "package": PACKAGE_NAME,
        "version": VERSION,
        "version_code": VERSION_CODE,
        "orientation": ORIENTATION,
        "min_android": MIN_ANDROID_VERSION,
        "target_android": TARGET_ANDROID_VERSION,
        "inputs": SUPPORTED_INPUTS,
        "graphics_modes": GRAPHICS_MODES,
        "default_graphics": DEFAULT_GRAPHICS_MODE,
        "fps": DEFAULT_FPS,
    }


def supports_input(input_type):

    return input_type in SUPPORTED_INPUTS


def supports_graphics(mode):

    return mode in GRAPHICS_MODES
