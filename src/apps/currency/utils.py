import logging

import click

logger = logging.getLogger("django.db.backends")


def log_added_currencies(currencies: set[tuple[str, str]]) -> None:
    max_len = max(len(s) for s, _ in currencies)
    empty_str = f"{' ' * 5}"

    base_message = empty_str + "Added new currencies:" + empty_str
    color_base_message = click.style(base_message, fg="blue")

    # fmt: off
    rows = "\n".join(
        empty_str + f"{symbol.ljust(max_len)} - {name}"
        for symbol, name in currencies
    )
    color_rows = "\n".join(
        empty_str + f"{click.style(symbol.ljust(max_len), fg='bright_white', bold=True)} - {name}"
        for symbol, name in currencies
    )
    # fmt: on

    row = f"\n{'-' * len(base_message)}\n"
    message = f"\n{row}{base_message}\n{rows}{row}"
    color_message = f"\n{row}{color_base_message}\n{color_rows}{row}"

    logger.info(message, extra={"color_message": color_message})
