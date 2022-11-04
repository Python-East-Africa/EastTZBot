from pyrogram import Client, filters,enums
from pyrogram.types import (
    CallbackQuery,
    Chat,
    ChatPermissions,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)
import asyncio
from datetime import datetime

########## DELETE SPAM ##########


@Client.on_message(filters.regex(r"t\.me\/[-a-zA-Z0-9.]+(\/\S*)?"))
async def spam(client: Client, message: Message):

    user = await client.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )

    if (
        user.status == enums.ChatMemberStatus.OWNER
        or user.status == enums.ChatMemberStatus.ADMINISTRATOR
    ):
        return

    await message.delete()


@Client.on_message(filters.forwarded)
async def forwaded(client: Client, message: Message):
    user = await client.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )

    if (
        user.status == enums.ChatMemberStatus.OWNER
        or user.status == enums.ChatMemberStatus.ADMINISTRATOR
    ):
        return

    await message.delete()
