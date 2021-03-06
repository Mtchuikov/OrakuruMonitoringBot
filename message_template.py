# -*- coding: utf-8 -*-

from dataclasses import dataclass
from string import Template

__all__ = [
    'MessageTemplate',
]


@dataclass(frozen=True)
class MessageTemplate:
    welcome = (
        "You are welcome, samurai š"
    )

    ask_address = (
        "Samurai š, enter validators address\nto get information about it"
    )

    validator_stats = Template(
        "Samurai š, validator information\nreceived successfully\n\n"
        'ā  Validator <a href="https://testnet.bscscan.com/address/%s"><b>$address</b></a>\n'
        "āāāā Score: $score\n"
        "āāāā Total responses: $responses\n"
        "āāāā Response time: $response_time\n"
    )

    validator_not_found = (
        "Sorry Samurai š, we can't find\na validator with specified address"
    )

    leaderboard_title = Template(
        "Leaderboard. Page $current_page/$total_pages\n"
    )

    leaderboard_text = Template(
        '\nā  Validator <a href="https://testnet.bscscan.com/address/%s"><b>$address</b></a>\n'
        "āāāā Score: $score\n"
        "āāāā Total responses: $responses\n"
        "āāāā Response time: $response_time\n"
    )