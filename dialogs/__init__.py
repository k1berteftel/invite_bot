from dialogs.user_dialog.dialog import user_dialog
from dialogs.admin_dialog.dialog import admin_dialog
# Импорт админского диалога

def get_dialogs():
    return [admin_dialog, user_dialog]