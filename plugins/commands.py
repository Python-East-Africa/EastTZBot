from pyrogram import Client, filters
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


########## CUSTOM FILTER TO IDENTIFY ADMINS ##########


async def check_admin_filter(_, client: Client, message: Message):
    user = await client.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )
    return bool(
        user.status == enums.ChatMemberStatus.OWNER
        or user.status == enums.ChatMemberStatus.ADMINISTRATOR
    )


check_admin = filters.create(check_admin_filter)


########## HELP COMMAND ##########


@Client.on_message(
    filters.command(commands="help", prefixes=["/", "#", "!"], case_sensitive=False)
)
@Client.on_callback_query(filters.regex(r"helpmenu"))
async def help_menu_function(client, message):

    to_respond = "reply" if type(message) == Message else "edit_message_text"

    if to_respond == "edit_message_text":
        await message.answer()
    if to_respond == "reply":
        await message.delete()

    await getattr(message, to_respond)(
        text="Karibu Python East Africa",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Sheria",
                        callback_data="sheria.helpresponse",
                    ),
                    InlineKeyboardButton(
                        "Madini",
                        callback_data="madini.helpresponse",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Nakili",
                        callback_data="nakili.helpresponse",
                    ),
                    InlineKeyboardButton(
                        "Zaidi",
                        callback_data="extras",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Administration",
                        callback_data="adminmenu",
                    ),
                ],
            ]
        ),
    )


RESOURCES = """
**Rasilimali nzuri za Python kwa ajili ya kujifunza:**

• [Official Tutorial](https://docs.python.org/3/tutorial/index.html) - Book
• [Dive Into Python 3](https://www.diveinto.org/python3/table-of-contents.html) - Book
• [Hitchhiker's Guide!](https://docs.python-guide.org) - Book
• [Learn Python](https://www.learnpython.org/) - Interactive
• [Project Python](http://projectpython.net) - Interactive
• [Python Video Tutorials](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU) - Video
• [MIT OpenCourseWare](http://ocw.mit.edu/6-0001F16) - Course
• @PythonRes - Channel
"""

RULES = """
**Kanuni za Kikundi:**

1.Hiki ni kikundi cha Python. Majadiliano yote yanapaswa kuhusiana na Python.

2.Majadiliano ya lugha nyingine ni marufuku.

3.Yeyote atakayechapisha au kusambaza nyenzo zozote zinazohusiana na betting, skrill, dent, forex, sarafu za crypto nk zitaondolewa mara moja.

4.Kuomba programu, programu au vifaa vya utapeli ni marufuku isipokuwa swali linahusiana na Python.

5.Ikiwa unahitaji msaada na code yako, tumia site kama [Nekobin](https://nekobin.com).

6.Unaweza kutumia Kiingereza au Kiswahili katika kikundi hiki.

7.Kundi hili limekusudiwa kwa wale wanaojua au wanataka kujifunza Python.

8.Ikiwa unahitaji vifaa vya kujifunzia, tafuta kikundi kwa kutumia #resources

9.Maswali yote yanapaswa kuulizwa katika Kikundi. Hauruhusiwi kumfuata mtu inbox na kumuulliza..

10.Yeyote atakayekwenda kinyume na sheria zetu ataonywa au kuondolewa. Tunataka kutoa njia kwa watu kujifunza Python katika Afrika Mashariki.

"""

NAKILI = """
Tuma code au traceback kutumia orodha tofauti zilizopendekezwa

- https://nekobin.com/
- https://del.dog
- https://dpaste.org
- https://linkode.org
- https://hastebin.com
- https://bin.kv2.dev
"""

HELP_SWITCHER = {
    "sheria": RULES,
    "nakili": NAKILI,
    "madini": RESOURCES,
}


@Client.on_message(
    filters.command(commands=["sheria", "madini", "nakili"], prefixes=["#", "!", "/"])
)
@Client.on_callback_query(filters.regex(r"helpresponse"))
async def help_menu_response(client: Client, query):

    to_respond = "reply" if type(query) == Message else "edit_message_text"

    if to_respond == "edit_message_text":
        await query.answer()
        queried = query.data.split(".")[0]

    if to_respond == "reply":
        await query.delete()
        queried = query.text.split()[0].strip("#").strip("/").strip("!")

    await getattr(query, to_respond)(
        text=HELP_SWITCHER[queried],
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Back To Menu",
                        callback_data=f"helpmenu",
                    ),
                ]
            ]
        ),
    )


@Client.on_callback_query(filters.regex(r"adminmenu"))
async def admin_help_function(client: Client, query: CallbackQuery):

    queried = query.data.split(".")[0]
    await query.answer()
    await query.edit_message_text(
        text="Here are the Administrative Commands:",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Nyamaza",
                        callback_data="mute.adminresponse",
                    ),
                    InlineKeyboardButton(
                        "Fukuza",
                        callback_data="ban.adminresponse",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Futa",
                        callback_data="delete.adminresponse",
                    ),
                    InlineKeyboardButton(
                        "Nje",
                        callback_data="offtopic.adminresponse",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Soma",
                        callback_data="read.adminresponse",
                    ),
                    InlineKeyboardButton(
                        "Uliza",
                        callback_data="ask.adminresponse",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Back To Menu",
                        callback_data=f"helpmenu",
                    ),
                ],
            ]
        ),
    )


ADMIN_HELP_SWITCHER = {
    "mute": "Jibu message na **`/nyamaza`** kumnyamazisha mwandishi wa hio message",
    "ban": "Ijibu message na  **`/fukuza`** kumfukuza mwandishi wa hio message",
    "delete": "Ijibu message na **`/futa`** kuifuta hio message message",
    "offtopic": "Ijibu message na **`/nje`** kumuonya mwandishi",
    "read": "Ijibu message na **`/soma`** kumshwawishi mwandishi kusoma",
    "ask": "Ijibu message na **`/uliza`** kumfunza mwandishi namna ya kuuliza maswali",
}


@Client.on_callback_query(filters.regex(r"adminresponse"))
async def admin_response_function(client: Client, query: CallbackQuery):

    queried = query.data.split(".")[0]
    await query.answer()
    await query.edit_message_text(
        text=ADMIN_HELP_SWITCHER[queried],
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Back",
                        callback_data="adminmenu",
                    ),
                    InlineKeyboardButton(
                        "Help Menu",
                        callback_data="helpmenu",
                    ),
                ]
            ]
        ),
    )


########## MUTE COMMAND ##########


@Client.on_message(
    filters.command(commands=["mute", "nyamaza"], prefixes=["!", "/", "#"])
    & check_admin
)
async def mute(client: Client, message: Message):

    if not message.reply_to_message:
        return

    user = await client.get_chat_member(
        chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id
    )

    if (
        user.status == enums.ChatMemberStatus.OWNER
        or user.status == enums.ChatMemberStatus.ADMINISTRATOR
    ):
        message_to_reply = await message.reply(text="Sinyamazishi wasmimamizi")
        await asyncio.sleep(5)
        await message_to_reply.delete()
        await message.delete()
        return

    await message.reply_to_message.delete()
    await client.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        ChatPermissions(),
        datetime.now() + timedelta(hours=6),
    )
    await message.reply(
        text=f"[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) amenyamazishwa kwa masaa 6.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Unmute", f"unmute.{message.reply_to_message.from_user.id}"
                    )
                ]
            ]
        ),
    )


@Client.on_callback_query(filters.regex(r"unmute"))
async def unmute(client: Client, query: CallbackQuery):

    to_be_unmuted = query.data.split(".")[1]
    text = query.message.text

    user = await client.get_chat_member(
        chat_id=query.message.chat.id, user_id=query.from_user.id
    )

    if not (
        user.status == enums.ChatMemberStatus.OWNER
        or user.status == enums.ChatMemberStatus.ADMINISTRATOR
    ):
        await query.answer("Hii ni kazi ya wasimamizi!", show_alert=True)
        return

    await client.restrict_chat_member(
        query.message.chat.id,
        to_be_unmuted,
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

    await query.edit_message_text(f"~~{text.markdown}~~\n\nUmesamehewa!")


######## BAN COMMAND ########


@Client.on_message(
    filters.command(commands=["ban", "fukuza"], prefixes=["!", "/", "#"]) & check_admin
)
async def ban(client: Client, message: Message):

    if not message.reply_to_message:
        return

    user = await client.get_chat_member(
        chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id
    )

    if (
        user.status == enums.ChatMemberStatus.OWNER
        or user.status == enums.ChatMemberStatus.ADMINISTRATOR
    ):
        message_to_reply = await message.reply(
            text="Sina mamlaka ya kufukuza wasimamizi"
        )
        await asyncio.sleep(5)
        await message_to_reply.delete()
        await message.delete()
        return

    await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply_to_message.delete()
    await message.reply(
        text=f"[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) amefukuzwa.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Unban", f"unban.{message.reply_to_message.from_user.id}"
                    )
                ]
            ]
        ),
    )


@Client.on_callback_query(filters.regex(r"unban"))
async def unban(client: Client, query: CallbackQuery):

    to_be_unbanned = query.data.split(".")[1]
    text = query.message.text

    user = await client.get_chat_member(
        chat_id=query.message.chat.id, user_id=query.from_user.id
    )

    if not (
        user.status == enums.ChatMemberStatus.OWNER
        or user.status == enums.ChatMemberStatus.ADMINISTRATOR
    ):
        await query.answer("Hii ni kazi ya wasimamizi!", show_alert=True)
        return

    await client.unban_chat_member(query.message.chat.id, to_be_unbanned)

    await query.edit_message_text(f"~~{text.markdown}~~\n\nUmesamehewa")


########## DELETE MESSAGES ##########
@Client.on_message(
    filters.command(commands=["delete", "futa"], prefixes=["!", "/", "#"]) & check_admin
)
async def delete_a_message(client: Client, message: Message):

    if not message.reply_to_message:
        await message.delete()
        return
    await message.delete()
    await message.reply_to_message.delete()


########## OFFTOPIC MESSAGES ##########
@Client.on_message(
    filters.command(commands=["offtopic", "nje"], prefixes=["!", "/", "#"])
    & check_admin
)
async def nje_ya_mada(client: Client, message: Message):

    if not message.reply_to_message:
        await message.delete()
        return
    await message.delete()
    await message.reply(
        text="Hoja hii haihusiani na Python",
        reply_to_message_id=message.reply_to_message.id,
    )


########## HOW TO ASK ##########
@Client.on_message(
    filters.command(commands=["ask", "uliza"], prefixes=["!", "/", "#"]) & check_admin
)
async def namna_ya_kuuliza(client: Client, message: Message):

    if not message.reply_to_message:
        await message.delete()
        return
    await message.delete()
    await message.reply(
        text="""
Samahani, swali lako halijaundwa vizuri. Tafadhali, fuata miongozo katika kiungo hapa chini.
[Ninaulizaje swali zuri?](https://stackoverflow.com/help/how-to-ask)
""",
        reply_to_message_id=message.reply_to_message.id,
    )


########## READ ##########
@Client.on_message(
    filters.command(commands=["read", "soma"], prefixes=["!", "/", "#"]) & check_admin
)
async def nje_ya_mada(client: Client, message: Message):

    if not message.reply_to_message:
        await message.delete()
        return
    await message.delete()
    await message.reply_photo(
        photo="read.jpg",
        caption="Tafadhali, soma nyaraka za python: https://docs.python.org",
        reply_to_message_id=message.reply_to_message.id,
    )



