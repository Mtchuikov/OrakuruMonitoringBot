# -*- coding: utf-8 -*-

from dataclasses import dataclass
from string import Template

__all__ = [
    'MessageTemplate',
]


@dataclass(frozen=True)
class MessageTemplate:
    welcome = (
        "You are welcome, samurai 🐙"
    )

    ask_address = (
        "Samurai 🐙, enter validators address\nto get information about it"
    )

    validator_stats = Template(
        "Samurai 🐙, validator information\nreceived successfully\n\n"
        '┌  Validator <a href="https://testnet.bscscan.com/address/%s"><b>$address</b></a>\n'
        "├─── Score: $score\n"
        "├─── Total responses: $responses\n"
        "└─── Response time: $response_time\n"
    )

    validator_not_found = (
        "Sorry Samurai 🐙, we can't find\na validator with specified address"
    )

    leaderboard_title = Template(
        "Leaderboard. Page $current_page/$total_pages\n"
    )

    leaderboard_text = Template(
        '\n┌  Validator <a href="https://testnet.bscscan.com/address/%s"><b>$address</b></a>\n'
        "├─── Score: $score\n"
        "├─── Total responses: $responses\n"
        "└─── Response time: $response_time\n"
    )