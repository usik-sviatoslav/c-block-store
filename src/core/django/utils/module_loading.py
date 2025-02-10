import os

__all__ = [
    "settings_module",
]


def _get_settings_module() -> str:
    env_state = os.getenv("ENV_STATE", "development")

    module_map = {
        "development": "core.django.settings.development",
        "production": "core.django.settings.production",
        "staging": "core.django.settings.staging",
    }

    return module_map.get(env_state, module_map["development"])


settings_module = _get_settings_module()
