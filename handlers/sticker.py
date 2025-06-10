import os
import logging
from typing import Optional
from telegram import Update, Sticker, StickerSet, InputSticker
from telegram.ext import ContextTypes
from PIL import Image
import webptools
from io import BytesIO
import requests
from config import Config

logger = logging.getLogger(__name__)

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming stickers and provide kang option."""
    if not update.message or not update.message.sticker:
        return
    
    user = update.message.from_user
    logger.info(f"Sticker received from {user.id} ({user.username})")
    
    await update.message.reply_text(
        "Nice sticker! Use /kang to add it to your pack or /mmf to meme it."
    )

async def kang_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add sticker to user's pack."""
    if not update.message or not update.message.reply_to_message or not update.message.reply_to_message.sticker:
        await update.message.reply_text("Please reply to a sticker to kang it.")
        return
    
    user = update.message.from_user
    sticker = update.message.reply_to_message.sticker
    
    try:
        # Download sticker
        sticker_file = await context.bot.get_file(sticker.file_id)
        sticker_bytes = await sticker_file.download_as_bytearray()
        
        # Process sticker
        if sticker.is_animated or sticker.is_video:
            await update.message.reply_text("Animated/video stickers are not supported yet.")
            return
        
        # Convert to PNG if needed
        if sticker.mime_type == "image/webp":
            with Image.open(BytesIO(sticker_bytes)) as img:
                output = BytesIO()
                img.save(output, format="PNG")
                png_bytes = output.getvalue()
        else:
            png_bytes = sticker_bytes
        
        # Create or add to sticker set
        pack_name = Config.STICKER_PACK_NAME.format(username=user.username)
        pack_title = Config.STICKER_PACK_TITLE.format(username=user.username)
        
        # Check if sticker set exists
        try:
            sticker_set = await context.bot.get_sticker_set(pack_name)
            emojis = sticker.emoji if sticker.emoji else "👍"
            
            # Add sticker to existing set
            await context.bot.add_sticker_to_set(
                user_id=user.id,
                name=pack_name,
                sticker=InputSticker(
                    png_sticker=png_bytes,
                    emoji_list=[emojis]
                )
            )
            await update.message.reply_text(
                f"Sticker added to your pack! View it [here](https://t.me/addstickers/{pack_name})",
                parse_mode="Markdown"
            )
        except Exception as e:
            # Create new sticker set
            await context.bot.create_new_sticker_set(
                user_id=user.id,
                name=pack_name,
                title=pack_title,
                stickers=[InputSticker(
                    png_sticker=png_bytes,
                    emoji_list=[sticker.emoji if sticker.emoji else "👍"]
                )],
                sticker_format="static" if not sticker.is_animated else "animated"
            )
            await update.message.reply_text(
                f"New sticker pack created! View it [here](https://t.me/addstickers/{pack_name})",
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Error kanging sticker: {e}")
        await update.message.reply_text("Failed to kang sticker. Please try again.")
