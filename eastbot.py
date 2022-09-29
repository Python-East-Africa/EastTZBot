from pyrogram import Client, emoji, filters, enums
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
from random import sample, shuffle

app = Client("easbot")

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


@app.on_message(filters.new_chat_members)
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


@app.on_callback_query(filters.regex(r"captcha"))
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


@app.on_message(filters.left_chat_member)
async def member_left_group(client, message):
    await message.delete()


########## HELP COMMAND ##########


@app.on_message(
    filters.command(commands="help", prefixes=["/", "#", "!"], case_sensitive=False)
)
@app.on_callback_query(filters.regex(r"helpmenu"))
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


@app.on_message(
    filters.command(commands=["sheria", "madini", "nakili"], prefixes=["#", "!", "/"])
)
@app.on_callback_query(filters.regex(r"helpresponse"))
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


@app.on_callback_query(filters.regex(r"adminmenu"))
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


@app.on_callback_query(filters.regex(r"adminresponse"))
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


@app.on_message(
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


@app.on_callback_query(filters.regex(r"unmute"))
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


@app.on_message(
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


@app.on_callback_query(filters.regex(r"unban"))
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
@app.on_message(
    filters.command(commands=["delete", "futa"], prefixes=["!", "/", "#"]) & check_admin
)
async def delete_a_message(client: Client, message: Message):

    if not message.reply_to_message:
        await message.delete()
        return
    await message.delete()
    await message.reply_to_message.delete()


########## OFFTOPIC MESSAGES ##########
@app.on_message(
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
@app.on_message(
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
@app.on_message(
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


########## EXTRA FEATURES ##########


@app.on_callback_query(filters.regex(r"extras"))
async def help_menu_response(client: Client, query: CallbackQuery):

    await query.answer()
    await query.edit_message_text(
        text="Here are some extra goodies",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Puzzle",
                        callback_data="puzzle-start",
                    ),
                    InlineKeyboardButton(
                        "Help Menu",
                        callback_data="helpmenu",
                    ),
                ]
            ]
        ),
    )


########## PUZZLE ###############


answer_list = [
    "KEYCAP_DIGIT_ONE",
    "KEYCAP_DIGIT_TWO",
    "KEYCAP_DIGIT_THREE",
    "KEYCAP_DIGIT_FOUR",
    "KEYCAP_DIGIT_FIVE",
    "KEYCAP_DIGIT_SIX",
    "KEYCAP_DIGIT_SEVEN",
    "KEYCAP_DIGIT_EIGHT",
    "WHITE_LARGE_SQUARE",
]
answer_list = [emoji.__getattribute__(e) for e in answer_list]


def output(list1):

    return f"{list1[0]}\t\t\t{list1[1]}\t\t\t{list1[2]}\n\n\n{list1[3]}\t\t\t{list1[4]}\t\t\t{list1[5]}\n\n\n{list1[6]}\t\t\t{list1[7]}\t\t\t{list1[8]}"


def produce_9number():

    while True:

        list1 = [
            "KEYCAP_DIGIT_ONE",
            "KEYCAP_DIGIT_TWO",
            "KEYCAP_DIGIT_THREE",
            "KEYCAP_DIGIT_FOUR",
            "KEYCAP_DIGIT_FIVE",
            "KEYCAP_DIGIT_SIX",
            "KEYCAP_DIGIT_SEVEN",
            "KEYCAP_DIGIT_EIGHT",
            "WHITE_LARGE_SQUARE",
        ]
        list1 = [emoji.__getattribute__(e) for e in list1]

        list2 = []
        shuffle(list1)
        # to make sure it is solvable, the inverse number must be even
        inverse_number = 0
        for i in list1:
            list2.append(i)
        list2.remove(emoji.__getattribute__("WHITE_LARGE_SQUARE"))
        for n in range(7):
            for i in range(n + 1, 8):
                if list2[n] > list2[i]:
                    inverse_number += 1
        if inverse_number % 2 == 0:
            return list1, output(list1)
        # if the inverse number is odd, then reproduce the puzzle
        else:
            continue


def move(p_number, p_puzzle_number, instruction, list1):
    for i in range(p_puzzle_number):
        if list1[i] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
            a = i
    if instruction == "l":
        list1[a], list1[a + 1] = list1[a + 1], list1[a]
        return output(list1)
    if instruction == "r":
        list1[a], list1[a - 1] = list1[a - 1], list1[a]
        return output(list1)
    if instruction == "u":
        list1[a], list1[a + p_number] = list1[a + p_number], list1[a]
        return output(list1)
    if instruction == "d":
        list1[a], list1[a - p_number] = list1[a - p_number], list1[a]
        return output(list1)


@app.on_callback_query(filters.regex(r"puzzle-start"))
async def start(client: Client, query: CallbackQuery):

    list1, message_output = produce_9number()
    await query.edit_message_text(
        text="`" + message_output + "`",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Up", callback_data=f"u.puzzle-game")],
                [
                    InlineKeyboardButton("Left", callback_data=f"l.puzzle-game"),
                    InlineKeyboardButton("Right", callback_data=f"r.puzzle-game"),
                ],
                [InlineKeyboardButton("Down", callback_data=f"d.puzzle-game")],
            ]
        ),
    )


@app.on_callback_query(filters.regex(r"puzzle-game"))
async def instruction_move_9(client: Client, query: CallbackQuery):

    list1 = query.message.text.split()

    await query.answer()

    instruction = query.data.split(".")[0]

    if list1[0] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == "d" or instruction == "r":
            return
    if list1[1] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == "d":
            return
    if list1[2] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == "d" or instruction == "l":
            return
    if list1[3] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == "r":
            return
    if list1[4] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        pass
    if list1[5] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == "l":
            return
    if list1[6] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == "r" or instruction == "u":
            return
    if list1[7] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == "u":
            return
    if list1[8] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if list1 == answer_list:
            pass
        else:
            if instruction == "l" or instruction == "u":
                return
    try:

        await query.edit_message_text(
            text="`" + move(3, 9, instruction, list1) + "`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Up", callback_data="u.puzzle-game")],
                    [
                        InlineKeyboardButton("Left", callback_data="l.puzzle-game"),
                        InlineKeyboardButton("Right", callback_data="r.puzzle-game"),
                    ],
                    [InlineKeyboardButton("Down", callback_data="d.puzzle-game")],
                ]
            ),
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)

    if list1 == answer_list:
        await query.edit_message_text(
            text="Congratulations! You have solved the Puzzle"
        )
        return


########## DELETE SPAM ##########


@app.on_message(filters.regex(r"t\.me\/[-a-zA-Z0-9.]+(\/\S*)?"))
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


@app.on_message(filters.forwarded)
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


app.run()
