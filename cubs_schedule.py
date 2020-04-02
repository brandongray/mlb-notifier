#!/usr/bin/python

import statsapi
import datetime
from dateutil import tz
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
destinations = os.environ.get("DESTINATIONS")
from_email = os.environ.get("FROM_EMAIL")

team = statsapi.lookup_team('chc')[0]
today = datetime.date.today().strftime("%m/%d/%Y")

games = statsapi.schedule(team=team["id"], date=today)

from_zone = tz.tzutc()
to_zone = tz.gettz("America/Chicago")

for game in games:
    dt = datetime.datetime.strptime(game["game_datetime"], "%Y-%m-%dT%H:%M:%SZ")
    time = dt.replace(tzinfo=from_zone).astimezone(to_zone).strftime('%I:%M %p')
    message = "{} at {}".format(game["summary"], time)
    
    email_message = Mail(
        from_email=from_email,
        to_emails=destinations,
        subject="MLB",
        html_content=message
    )

    response = sg.send(email_message)