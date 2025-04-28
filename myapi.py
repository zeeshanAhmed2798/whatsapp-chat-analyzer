def fetch_results(df):
    from openai import OpenAI

    # Initialize the OpenAI client with OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
        # Replace with your actual API key
    )

    # WhatsApp group messages (truncated for brevity; replace with full data)
    # Combine all messages into one big paragraph
    all_messages = ' '.join(df['message'].tolist())

    # Now you can use 'all_messages' in your API prompt

    # Define the analysis prompt
    analysis_prompt = f"""
    Analyze the following WhatsApp group messages and provide structured insights not add line like Let me know if you'd like deeper analysis on specific segments! in last:

    ### Input Messages:
    {all_messages}

    ### Tasks:
    1. **Categorize Topics**: Identify key discussion topics (e.g., Academics, Logistics, Casual Chat).
    2. **Interaction Types**: Classify messages (e.g., Announcements, Queries, Commands, Jokes).
    3. **Sentiment Trends**: Highlight positive/negative/neutral tones (use emojis as cues).
    4. **Key Entities**: Extract important names, deadlines, or events.
    5. **Summary**: A concise paragraph summarizing the group's activity.

    ### Output Format:
    - **Topics**: [Comma-separated list]
    - **Interactions**: [Comma-separated list]
    - **Sentiment**: [Positive/Negative/Neutral dominant]
    - **Entities**: [List of names/dates/events]
    - **Summary**: [1-2 paragraph analysis]
    """

    # Generate the analysis
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://example.com",  # Replace with your site
            "X-Title": "WhatsApp Analyzer",  # Optional
        },
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": "You are a data analyst specializing in chat message analysis."},
            {"role": "user", "content": analysis_prompt}
        ],
        temperature=0.3,  # Reduce randomness for factual analysis
    )

    # Print the results
    return(completion.choices[0].message.content)