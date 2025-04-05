import pandas as pd
import re
from io import StringIO

def parse_chat(file):
    data = file.read().decode("utf-8")

    # Normalize unicode spaces (e.g., narrow no-break space → normal space)
    data = data.replace("\u202f", " ").replace("\xa0", " ")

    messages = []
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} (AM|PM)) - ([^:]+): (.*)"

    for line in data.split("\n"):
        match = re.match(pattern, line)
        if match:
            datetime_str, _, sender, msg = match.groups()
            messages.append((datetime_str, sender.strip(), msg.strip()))

    df = pd.DataFrame(messages, columns=["datetime", "sender", "message"])
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    participants = df["sender"].unique().tolist()
    return df, participants
