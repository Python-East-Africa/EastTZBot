from pyrogram import Client, filters,emoji
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
from random import shuffle


########## EXTRA FEATURES ##########


@Client.on_callback_query(filters.regex(r"extras"))
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


@Client.on_callback_query(filters.regex(r"puzzle-start"))
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


@Client.on_callback_query(filters.regex(r"puzzle-game"))
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
        await asyncio.sleep(60)
        await query.message.delete()
        return
