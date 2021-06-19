# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(frozen=True)
class Message:

    welcome: str = 'You are welcome, samurai 🐙'


    ask_address: str = 'Samurai 🐙, enter validators address\nto get information about it'

    validator_statistic: str = (
        'Samurai 🐙, validator information\nreceived successfully\n\n'
        '┌ Rank: %s\n'
        '├─ Validator <a href="https://testnet.bscscan.com/address/%s"><b>%s</b></a>\n'
        '├─── Score: %s\n'
        '├─── Total responses: %s\n'
        '└─── Response time: %s\n'
    )

    validator_not_found: str = "Sorry Samurai 🐙, we can't find\na validator with specified address"


    leaderboard_title: str = 'Leaderboard. Page %s/%s\n'
    
    leaderboard_note: str = (
      '\n┌ Rank: %s\n'
        '├─ Validator <a href="https://testnet.bscscan.com/address/%s"><b>%s</b></a>\n'
        '├─── Score: %s\n'
        '├─── Total responses: %s\n'
        '└─── Response time: %s\n'
    )


message = Message


