import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud


def generate_stats(df):
    stats = {
        "Total Messages": df.shape[0],
        "Total Words": df["message"].str.split().str.len().sum(),
        "Media Shared": df["message"].str.contains("<Media omitted>").sum(),
        "Links Shared": df["message"].str.contains("http").sum(),
    }
    return stats


def plot_activity(df):
    df["hour"] = df["datetime"].dt.hour
    df["weekday"] = df["datetime"].dt.day_name()
    df["month"] = df["datetime"].dt.month_name()

    st.subheader("Messages by Hour")
    st.bar_chart(df["hour"].value_counts().sort_index())

    st.subheader("Messages by Weekday")
    st.bar_chart(
        df["weekday"]
        .value_counts()
        .reindex(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
    )

    # Generate Word Cloud only if there's valid text
    all_text = " ".join(df["message"].dropna().astype(str).tolist()).strip()
    if all_text:
        wordcloud = WordCloud(width=800, height=400).generate(all_text)
        st.image(wordcloud.to_array(), caption="Word Cloud")
    else:
        st.info("Not enough text data to generate a word cloud.")
