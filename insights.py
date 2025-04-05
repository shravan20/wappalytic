import random
import numpy as np


def funny_insights(df, participants):
    insights = []
    msg_counts = df["sender"].value_counts()

    if msg_counts.empty:
        return ["Not enough chat data to generate insights."]

    # Safe to proceed
    most_talkative = msg_counts.idxmax()
    quietest = msg_counts.idxmin()
    insights.append(
        f"**{most_talkative}** is the most talkative. Probably needs a podcast."
    )
    insights.append(f"**{quietest}** is either mysterious or too cool to reply.")

    sorry_count = df[df["message"].str.lower().str.contains("sorry", na=False)][
        "sender"
    ].value_counts()
    if not sorry_count.empty:
        insights.append(
            f"**{sorry_count.idxmax()}** says sorry the most. A certified apologizer."
        )

    love_count = df[df["message"].str.lower().str.contains("love", na=False)][
        "sender"
    ].value_counts()
    if not love_count.empty:
        insights.append(f"**{love_count.idxmax()}** spreads love like Nutella.")

    df["date"] = df["datetime"].dt.date
    streaks = df.groupby("sender")["date"].nunique()
    if not streaks.empty:
        longest = streaks.idxmax()
        insights.append(f"**{longest}** showed up the most number of days. Real MVP!")

    df["time_diff"] = df["datetime"].diff().dt.total_seconds().div(60).fillna(0)
    avg_reply_time = df.groupby("sender")["time_diff"].mean().sort_values()
    if not avg_reply_time.empty:
        insights.append(
            f"Fastest replier: **{avg_reply_time.idxmin()}**. Probably has your notifications ON."
        )
        insights.append(
            f"Slowest replier: **{avg_reply_time.idxmax()}**. Ghosting level: PRO."
        )

    # Funny quotes
    quotes_df = df[df["message"].str.len() > 20]
    if not quotes_df.empty:
        funny_quotes = quotes_df.sample(min(3, len(quotes_df)))
        insights += [
            f'Funny quote from {row.sender}: "{row.message}"'
            for _, row in funny_quotes.iterrows()
        ]

    return insights
