from pyrogram import Client, emoji, filters
from pyrogram.types import (
    CallbackQuery,
    Chat,
    ChatPermissions,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)
import asyncio
from datetime import datetime, timedelta
from random import sample

########## CAPTCHA AND WELCOME MESSAGE ##########

CAPTCHA_EMOJIS = [
    "SKULL",
    "ALARM_CLOCK",
    "WATERMELON",
    "SAFETY_PIN",
    "ROLL_OF_PAPER",
    "SPOON",
    "CUSTARD",
    "SNAIL",
    "BEER_MUG",
    "COFFIN",
    "BIRTHDAY_CAKE",
    "LOCKED",
    "MICROSCOPE",
    "TROPHY",
    "BOMB",
    "LOBSTER",
    "PIZZA",
    "HAMBURGER",
    "GOAT",
    "ROSE",
    "BANANA",
    "BASEBALL",
    "CAMERA",
    "DOG",
    "MAGNET",
    "RAINBOW",
    "TOMATO",
    "SNOWMAN",
    "BONE",
]

MENTION = "[{}](tg://user?id={})"

MESSAGE = "Karibu {}! Chagua emoji's unazoziona.Una dakika tatu na unaruhusiwa kukosea mara tatu tu."


@Client.on_message(filters.new_chat_members)
async def welcome(client, message):

    global captcha

    await message.delete()

    user_id = ",".join([str(u.id) for u in message.new_chat_members])
    user_id = int(user_id)

    await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())

    new_members = [MENTION.format(i.first_name, i.id) for i in message.new_chat_members]

    message_text = MESSAGE.format(", ".join(new_members))

    list_of_emojis = [e for e in sample(CAPTCHA_EMOJIS, 9)]

    list_of_emojis = [emoji.__getattribute__(e) for e in list_of_emojis]

    captcha = [e for e in sample(list_of_emojis, 3)]

    captcha_text = "      ".join(captcha)

    message_to_reply = await message.reply(
        f"{message_text}\n\n\n{captcha_text}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        list_of_emojis[0],
                        callback_data=f"{list_of_emojis[0]}.captcha",
                    ),
                    InlineKeyboardButton(
                        list_of_emojis[1],
                        callback_data=f"{list_of_emojis[1]}.captcha",
                    ),
                    InlineKeyboardButton(
                        list_of_emojis[2],
                        callback_data=f"{list_of_emojis[2]}.captcha",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        list_of_emojis[3],
                        callback_data=f"{list_of_emojis[3]}.captcha",
                    ),
                    InlineKeyboardButton(
                        list_of_emojis[4],
                        callback_data=f"{list_of_emojis[4]}.captcha",
                    ),
                    InlineKeyboardButton(
                        list_of_emojis[5],
                        callback_data=f"{list_of_emojis[5]}.captcha",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        list_of_emojis[6],
                        callback_data=f"{list_of_emojis[6]}.captcha",
                    ),
                    InlineKeyboardButton(
                        list_of_emojis[7],
                        callback_data=f"{list_of_emojis[7]}.captcha",
                    ),
                    InlineKeyboardButton(
                        list_of_emojis[8],
                        callback_data=f"{list_of_emojis[8]}.captcha",
                    ),
                ],
            ]
        ),
    )
    await asyncio.sleep(180)
    await message_to_reply.delete()


captcha_checker = set()  # will confirm our captcha
number_of_tries = 0  # kick user if it reaches 3


@Client.on_callback_query(filters.regex(r"captcha"))
async def captcha_function(client: Client, query):

    global captcha_checker, number_of_tries

    replier = query.from_user.id  # one who answered the captcha
    target = query.message.entities[0].user.id  # target of the captcha

    emoji_response = query.data.split(".")[0]

    if replier != target:
        await query.answer("Samahani,huu ujumbe si wako.", show_alert=True)
        return
    if emoji_response in captcha:
        captcha_checker.add(emoji_response)
        await query.answer(text="Sahihi!", cache_time=1)
        if len(captcha_checker) == len(captcha):
            new_welcome_message = await query.edit_message_text(
                f"Karibu Python East African Group [{query.from_user.first_name}](tg://user?id={target}).\n\nTafadhali Fata Sheria za Group. Bonyeza **`Help`** kupata msaada zaidi.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Help",
                                callback_data=f"helpmenu",
                            ),
                        ]
                    ]
                ),
            )
            await client.restrict_chat_member(
                query.message.chat.id,
                target,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                ),
            )
            captcha_checker = set()
            number_of_tries = 0

    elif number_of_tries == 2:
        await query.answer(
            "Umeshindwa kujithibitisha. Jaribu tena baadae.", show_alert=True
        )
        await asyncio.sleep(5)
        kicker = await client.ban_chat_member(
            query.message.chat.id,
            target,
            datetime.now() + timedelta(seconds=60),  # Kick user from chat for a minute
        )
        await kicker.delete()
        await query.message.delete()

        captcha_checker = set()
        number_of_tries = 0

    elif emoji_response not in captcha:
        await query.answer(text="Wrong!", cache_time=1)
        number_of_tries += 1


@Client.on_message(filters.left_chat_member)
async def member_left_group(client, message):
    await message.delete()
