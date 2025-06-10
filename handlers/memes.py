import logging
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap
import os

logger = logging.getLogger(__name__)

async def generate_meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate meme from sticker/image with text."""
    if not update.message:
        return
    
    # Check if replying to a message with sticker/image
    if not update.message.reply_to_message or not (
        update.message.reply_to_message.sticker or 
        update.message.reply_to_message.photo
    ):
        await update.message.reply_text("Please reply to a sticker or image with /mmf <top text> | <bottom text>")
        return
    
    # Get text input
    if not context.args:
        await update.message.reply_text("Please provide text in format: /mmf <top text> | <bottom text>")
        return
    
    text = " ".join(context.args)
    if "|" in text:
        top_text, bottom_text = text.split("|", 1)
    else:
        top_text = text
        bottom_text = ""
    
    try:
        # Get the image
        if update.message.reply_to_message.sticker:
            sticker = update.message.reply_to_message.sticker
            if sticker.is_animated or sticker.is_video:
                await update.message.reply_text("Animated/video stickers are not supported for memes.")
                return
            
            file = await context.bot.get_file(sticker.file_id)
            image_bytes = await file.download_as_bytearray()
            image = Image.open(BytesIO(image_bytes))
        else:
            # Get the highest resolution photo
            photo = update.message.reply_to_message.photo[-1]
            file = await context.bot.get_file(photo.file_id)
            image_bytes = await file.download_as_bytearray()
            image = Image.open(BytesIO(image_bytes))
        
        # Prepare meme
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        
        # Load font (you might need to provide a font file)
        try:
            font = ImageFont.truetype("impact.ttf", size=int(image_height / 10))
        except:
            font = ImageFont.load_default()
        
        # Draw top text
        if top_text.strip():
            top_text = top_text.strip().upper()
            char_width, char_height = font.getsize("A")
            chars_per_line = image_width // char_width
            top_lines = textwrap.wrap(top_text, width=chars_per_line)
            
            y = 10
            for line in top_lines:
                line_width, line_height = font.getsize(line)
                x = (image_width - line_width) / 2
                draw.text((x, y), line, fill="white", font=font, stroke_width=2, stroke_fill="black")
                y += line_height
        
        # Draw bottom text
        if bottom_text.strip():
            bottom_text = bottom_text.strip().upper()
            char_width, char_height = font.getsize("A")
            chars_per_line = image_width // char_width
            bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)
            
            y = image_height - (len(bottom_lines) * char_height) - 20
            for line in bottom_lines:
                line_width, line_height = font.getsize(line)
                x = (image_width - line_width) / 2
                draw.text((x, y), line, fill="white", font=font, stroke_width=2, stroke_fill="black")
                y += line_height
        
        # Save and send
        output = BytesIO()
        image.save(output, format="PNG")
        output.seek(0)
        
        await update.message.reply_photo(photo=output, caption="Here's your meme!")
        
    except Exception as e:
        logger.error(f"Error generating meme: {e}")
        await update.message.reply_text("Failed to generate meme. Please try again.")
