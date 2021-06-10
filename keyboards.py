from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)

MainMenuKeyboard = InlineKeyboardMarkup(row_width=1)
MainMenuKeyboard.add(
    InlineKeyboardButton(
        text='🌸 Sakura',
        callback_data='show_leaderboard'
    ),
    InlineKeyboardButton(
            text='🔎 Check validator',
            callback_data='check_validator'
        )
)


def TurnLeaderboardPageKeyboard(note_id: int, *last_note_id: int) -> object:
    TurnLeaderboardPageKeyboard = InlineKeyboardMarkup(row_width=2)

    if note_id == 1:
        TurnLeaderboardPageKeyboard.add(
            InlineKeyboardButton(
                text='🡺',
                callback_data='next_leaderboard_page'
            )
        )

    elif note_id == last_note_id:
        TurnLeaderboardPageKeyboard.add(
            InlineKeyboardButton(
                text='🡸', 
                callback_data='back_leaderboard_page'
            )
        )

    else:
        TurnLeaderboardPageKeyboard.add(
            InlineKeyboardButton(
                text='🡸',
                callback_data='back_leaderboard_page',
            ),
            InlineKeyboardButton(
                text='🡺',
                callback_data='next_leaderboard_page'
            )
        )

    TurnLeaderboardPageKeyboard.add(
        InlineKeyboardButton(
            text='🏠',
            callback_data='back_to_menu'
        )
    )

    return TurnLeaderboardPageKeyboard


BackHomeKeyboard = InlineKeyboardMarkup(row_width=1)
BackHomeKeyboard.add(
    InlineKeyboardButton(
        text='🏠',
        callback_data='back_to_menu'
    )
)

SearchValidatorAgainKeyboard = InlineKeyboardMarkup(row_width=1)
SearchValidatorAgainKeyboard.add(
    InlineKeyboardButton(
        text='Yes',
        callback_data='try_again'
    ),
    InlineKeyboardButton(
        text='No',
        callback_data='back_to_menu'
    )
)
