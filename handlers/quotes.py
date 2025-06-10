import logging
from typing import Optional
from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap
import os

logger = logging.getLogger(__name__)

async def quote_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Quote a message as a sticker/image."""
    if not update.message or not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to quote it.")
        return
    
    quoted_msg = update.message.reply_to_message
    user = quoted_msg.from_user
    
    try:
        # Create quote image
        width, height = 512, 512
        background_color = (30, 30, 46)  # Dark background
        text_color = (205, 214, 244)     # Light text
        
        image = Image.new("RGB", (width, height), background_color)
        draw = ImageDraw.Draw(image)
        
        # Load font (provide your font file)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
            name_font = ImageFont.truetype("arial.ttf", 24, "bold")
        except:
            font = ImageFont.load_default()
            name_font = ImageFont.load_default()
        
        # Draw user info
        if user.username:
            username = f"@{user.username}"
        else:
            username = f"{user.first_name} {user.last_name or ''}".strip()
        
        # Draw avatar if available
        avatar_bytes = None
        try:
            profile_photos = await context.bot.get_user_profile_photos(user.id, limit=1)
            if profile_photos.photos:
                photo = profile_photos.photos[0][-1]  # Get highest quality
                avatar_file = await context.bot.get_file(photo.file_id)
                avatar_bytes = await avatar_file.download_as_bytearray()
                avatar = Image.open(BytesIO(avatar_bytes))
                avatar = avatar.resize((50, 50))
                
                # Create circular mask
                mask = Image.new("L", (50, 50), 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.ellipse((0, 0, 50, 50), fill=255)
                
                # Paste avatar
                image.paste(avatar, (20, 20), mask)
        except Exception as e:
            logger.warning(f"Couldn't get profile photo: {e}")
        
        # Draw username
        draw.text((80, 30), username, fill=text_color, font=name_font)
        
        # Draw text
        text = quoted_msg.text or quoted_msg.caption or ""
        if not text and quoted_msg.sticker:
            text = "Sent a sticker"
        elif not text and quoted_msg.photo:
            text = "Sent a photo"
        elif not text and quoted_msg.video:
            text = "Sent a video"
        
        # Wrap text
        lines = textwrap.wrap(text, width=40)
        y = 80
        for line in lines:
            draw.text((20, y), line, fill=text_color, font=font)
            y += 30
            if y > height - 50:
                break
        
        # Save image
        output = BytesIO()
        image.save(output, format="PNG")
        output.seek(0)
        
        # Send as both photo and sticker
        await update.message.reply_photo(photo=output, caption="Quote as image")
        
        # Convert to sticker
        sticker_output = BytesIO()
        image.save(sticker_output, format="WEBP")
        sticker_output.seek(0)
        
        await update.message.reply_sticker(sticker=sticker_output)
        
    except Exception as e:
        logger.error(f"Error creating quote: {e}")
        await update.message.reply_text("Failed to create quote. Please try again.")
