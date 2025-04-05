import streamlit as st
from chat_parser import parse_chat
from analyzer import generate_stats, plot_activity
from insights import funny_insights
from chat_features import (
    sentiment_timeline,
    message_heatmap,
    tag_clouds_by_user,
    keyword_meter,
    longest_conversation,
    chat_awards,
)

st.set_page_config(page_title="wappalytic", layout="wide")
st.title("📱 Wappalytic (Offline)")

# Theme settings
theme = st.radio("🌗 Choose Theme", ["🌞 Light", "🌚 Dark"], horizontal=True)


def apply_theme(selected_theme):
    if selected_theme == "🌚 Dark":
        st.markdown(
            """
            <style>
                .stApp {
                    background-color: #1e1e1e;
                    color: #f0f0f0;
                }
                .css-18e3th9, .css-1d391kg {
                    background-color: #2a2a2a !important;
                    color: #f0f0f0;
                }
                .css-1v3fvcr {
                    background-color: #333333 !important;
                    color: #ffffff !important;
                }
                .e1fqkh3o3, .stMarkdown, .stDataFrame {
                    color: #e0e0e0 !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    # Optionally, add more custom styling for light mode if needed


apply_theme(theme)


with st.expander("📝 How to export your WhatsApp chat (.txt)"):
    st.markdown(
        """
        - On **Android**: Open the chat → Tap ⋮ → More → *Export Chat* → Choose **Without Media**.
        - On **iPhone**: Open the chat → Tap chat name → *Export Chat* → Choose **Without Media**.
        - Save or send the file to yourself (email, Google Drive, etc).
        - Then upload it below 👇
        """
    )

uploaded_file = st.file_uploader("Upload your WhatsApp chat .txt file", type=["txt"])

if uploaded_file:
    chat_df, participants = parse_chat(uploaded_file)

    if chat_df.empty:
        st.error(
            "No valid messages found. Please upload a properly exported WhatsApp chat (.txt) file."
        )
        st.stop()

    st.success("✅ Chat Parsed Successfully!")

    with st.expander("📊 Basic Stats"):
        stats = generate_stats(chat_df)
        st.json(stats)

    with st.expander("📈 Activity Analysis"):
        plot_activity(chat_df)

    with st.expander("💡 Funny & Deep Relationship Insights"):
        insights = funny_insights(chat_df, participants)
        for i in insights:
            st.markdown(f"- {i}")

    with st.expander("📅 Sentiment Timeline"):
        sentiment_timeline(chat_df)

    with st.expander("🔥 Message Heatmap"):
        message_heatmap(chat_df)

    with st.expander("🌈 Word Clouds Per Participant"):
        tag_clouds_by_user(chat_df)

    with st.expander("🎭 Love, Hate & Drama Meter"):
        keyword_meter(chat_df)

    with st.expander("🔁 Longest Chat Streak"):
        longest_conversation(chat_df)

    with st.expander("🏆 Chat Awards"):
        chat_awards(chat_df)
