import os

class Config:
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    PORT = int(os.getenv("PORT", 8443))
    ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
    
    # Sticker settings
    MAX_STICKER_SIZE = 512000  # 512KB
    STICKER_PACK_NAME = "kang_pack_by_{username}"
    STICKER_PACK_TITLE = "Kang Pack by @{username}"
