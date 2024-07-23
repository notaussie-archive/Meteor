import guilded
from datetime import datetime


def BasicErrorView(message: str):
    return guilded.Embed(
        title="Uh oh!",
        description=(
            message
            if message.endswith(
                (
                    "!",
                    ".",
                    "?",
                    "(",
                    ")",
                )
            )
            else message + "."
        ),
        color=guilded.Color.dark_theme(),
        timestamp=datetime.now(),
    )
