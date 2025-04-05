import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict
import streamlit as st

analyzer = SentimentIntensityAnalyzer()


def sentiment_timeline(df):
    df["date"] = df["datetime"].dt.date
    df["sentiment"] = df["message"].apply(
        lambda x: analyzer.polarity_scores(x)["compound"]
    )
    daily_sentiment = df.groupby("date")["sentiment"].mean()
    st.subheader("Chat Sentiment Timeline")
    st.line_chart(daily_sentiment)


def message_heatmap(df):
    df["date"] = df["datetime"].dt.date
    df["hour"] = df["datetime"].dt.hour
    heatmap_data = df.groupby(["date", "hour"]).size().unstack(fill_value=0)
    st.subheader("Message Heatmap")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data.T, cmap="YlGnBu", ax=ax)
    st.pyplot(fig)


def tag_clouds_by_user(df):
    st.subheader("Tag Cloud Per Participant")
    participants = df["sender"].unique()
    for person in participants:
        text = " ".join(df[df["sender"] == person]["message"].dropna().astype(str))
        if text:
            wc = WordCloud(width=600, height=300).generate(text)
            st.image(wc.to_array(), caption=f"Word Cloud for {person}")


def keyword_meter(df):
    st.subheader("Love, Hate & Drama Meter")
    keywords = ["love", "hate", "miss", "angry", "sorry"]
    counts = defaultdict(int)
    for keyword in keywords:
        counts[keyword] = df["message"].str.lower().str.contains(keyword).sum()
    st.bar_chart(pd.Series(counts))


def longest_conversation(df, max_gap_minutes=5):
    df_sorted = df.sort_values("datetime").copy()
    df_sorted["gap"] = df_sorted["datetime"].diff().dt.total_seconds().div(60).fillna(0)

    current_streak = []
    longest_streak = []

    for i, row in df_sorted.iterrows():
        if row["gap"] <= max_gap_minutes:
            current_streak.append(row)
        else:
            if len(current_streak) > len(longest_streak):
                longest_streak = current_streak
            current_streak = [row]

    if len(current_streak) > len(longest_streak):
        longest_streak = current_streak

    longest_df = pd.DataFrame(longest_streak)
    st.subheader("Longest Conversation Without a Break")
    st.write(
        f"Messages: {len(longest_df)}, Duration: {longest_df['datetime'].iloc[-1] - longest_df['datetime'].iloc[0]}"
    )
    st.dataframe(longest_df[["datetime", "sender", "message"]])


def chat_awards(df):
    st.subheader("Chat Awards")
    awards = []

    df["hour"] = df["datetime"].dt.hour
    night_owl = df[df["hour"] >= 0][df["hour"] <= 4]["sender"].value_counts().idxmax()
    awards.append(f"\U0001f319 Night Owl: **{night_owl}**")

    one_word = df[df["message"].str.split().str.len() == 1]["sender"].value_counts()
    if not one_word.empty:
        awards.append(f"💬 One-word Texter: **{one_word.idxmax()}**")

    long_msg = df[df["message"].str.len() > 100]["sender"].value_counts()
    if not long_msg.empty:
        awards.append(f"⌨️ Typing Marathoner: **{long_msg.idxmax()}**")

    starter = df.groupby("sender").head(1)["sender"].value_counts()
    if not starter.empty:
        awards.append(f"🚀 Conversation Starter: **{starter.idxmax()}**")

    for award in awards:
        st.markdown(f"- {award}")
