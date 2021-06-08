from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)

main_menu = InlineKeyboardMarkup(row_width=1)
main_menu.add(
    InlineKeyboardButton(
        text='🌸 Sakura',
        callback_data='show_leaderboard'
    ),
    InlineKeyboardButton(
            text='🔎 Check validator',
            callback_data='check_validator'
        )
)

switch_leaderboard_page = InlineKeyboardMarkup(row_width=2)
switch_leaderboard_page.add(
    InlineKeyboardButton(
        text='🡸',
        callback_data='back_leaderboard_page',
    ),
    InlineKeyboardButton(
        text='🡺',
        callback_data='next_leaderboard_page'
    ),
    InlineKeyboardButton(
        text='🏠',
        callback_data='back_to_menu'
    )
)

switch_leaderboard_next_page = InlineKeyboardMarkup(row_width=1)
switch_leaderboard_next_page.add(
    InlineKeyboardButton(
        text='🡺',
        callback_data='next_leaderboard_page'
    ),
    InlineKeyboardButton(
        text='🏠',
        callback_data='back_to_menu'
    )
)

switch_leaderboard_back_page = InlineKeyboardMarkup(row_width=1)
switch_leaderboard_back_page.add(
    InlineKeyboardButton(
        text='🡸',
        callback_data='back_leaderboard_page'
    ),
    InlineKeyboardButton(
        text='🏠',
        callback_data='back_to_menu'
    )
)

home_button = InlineKeyboardMarkup(row_width=1)
home_button.add(
    InlineKeyboardButton(
        text='🏠',
        callback_data='back_to_menu'
    )
)

paste_validator_address_again = InlineKeyboardMarkup(row_width=1)
paste_validator_address_again.add(
    InlineKeyboardButton(
        text='Yes',
        callback_data='try_again'
    ),
    InlineKeyboardButton(
        text='No',
        callback_data='back_to_menu'
    )
)
