import guilded
from humanfriendly import format_timespan
from datetime import datetime


def WelcomeBackView(data: dict):
    return guilded.Embed(
        title="Welcome back!",
        description="You were away for {}!".format(
            format_timespan(datetime.now() - data["timestamp"])
        ),
        color=guilded.Color.dark_theme(),
    )
