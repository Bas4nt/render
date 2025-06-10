import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import Config
from handlers import sticker, memes, quotes, admin

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(Config.TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", admin.start))
    application.add_handler(CommandHandler("help", admin.help))
    
    # Sticker handlers
    application.add_handler(MessageHandler(filters.Sticker.ALL, sticker.handle_sticker))
    application.add_handler(CommandHandler("kang", sticker.kang_sticker))
    application.add_handler(CommandHandler("mmf", memes.generate_meme))
    
    # Quote handlers
    application.add_handler(CommandHandler("quote", quotes.quote_message))
    
    # Admin handlers
    application.add_handler(CommandHandler("stats", admin.stats))
    
    # Start the bot
    if Config.WEBHOOK_URL:
        application.run_webhook(
            listen="0.0.0.0",
            port=Config.PORT,
            url_path=Config.TOKEN,
            webhook_url=f"{Config.WEBHOOK_URL}/{Config.TOKEN}"
        )
    else:
        application.run_polling()

if __name__ == "__main__":
    main()
