import os
from openai import OpenAI


# Initialize Groq client (OpenAI-compatible API)
def get_client():
    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")  # Store this in secrets
    )


def fetch_results(df):
    """
    Takes a dataframe with a 'message' column
    Returns structured WhatsApp chat analysis using Groq LLaMA 3.1
    """

    client = get_client()

    # Combine all messages into one large string
    all_messages = " ".join(df["message"].dropna().astype(str).tolist())

    # ⚠️ Optional safety: truncate very large chats (Groq models have token limits)
    MAX_CHAR_LENGTH = 12000
    if len(all_messages) > MAX_CHAR_LENGTH:
        all_messages = all_messages[:MAX_CHAR_LENGTH]

    analysis_prompt = f"""
Analyze the following WhatsApp group messages and provide structured insights only.

### Input Messages:
{all_messages}

### Tasks:
1. Categorize key discussion topics (Academics, Logistics, Casual Chat, etc.)
2. Classify interaction types (Announcements, Queries, Commands, Jokes, etc.)
3. Identify overall sentiment trend (Positive / Negative / Neutral)
4. Extract important entities (Names, Dates, Events)
5. Provide a short summary (1-2 paragraphs)

### Output Format:
- Topics: [Comma-separated list]
- Interactions: [Comma-separated list]
- Sentiment: [Dominant tone]
- Entities: [List]
- Summary: [Paragraph]
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional data analyst specializing in structured chat analysis."
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ],
            temperature=0.3,
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error occurred while generating analysis: {str(e)}"
