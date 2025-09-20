from pyrogram import Client, filters
from main import ALLOWED_USERS

# 🔒 Global user guard
@Client.on_message(filters.all)
async def guard(client, message):
    if message.from_user.id not in ALLOWED_USERS:
        # Unauthorized users को ignore कर दो
        return
