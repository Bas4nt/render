import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import Config

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=None
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
    🤖 <b>Group Manager Bot</b> 🤖

    <b>Commands:</b>
    /start - Start the bot
    /help - Show this help message
    /kang - Add replied sticker to your pack
    /mmf - Create meme from replied image/sticker
    /quote - Quote a message as sticker/image

    <b>Features:</b>
    • Kang stickers to your personal pack
    • Create memes with top/bottom text
    • Quote messages as beautiful images/stickers
    special thanks to @huehuekiki
    """
    await update.message.reply_html(help_text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send bot statistics."""
    if update.effective_user.id not in Config.ADMIN_IDS:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    
    stats_text = "📊 <b>Bot Statistics</b> 📊\n\n"
    stats_text += f"• Users: {0}\n"  # Add your stats tracking
    stats_text += f"• Groups: {0}\n"
    stats_text += f"• Stickers kanged: {0}\n"
    stats_text += f"• Memes generated: {0}\n"
    
    await update.message.reply_html(stats_text)
