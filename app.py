from flask import Flask, render_template_string, request, redirect, url_for
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download required NLTK data
nltk.download('vader_lexicon')

app = Flask(__name__)

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Store conversation history
conversation = []

# Define a simple route
@app.route("/", methods=["GET", "POST"])
def chatbot():
    global conversation
    if request.method == "POST":
        user_input = request.form.get("message")
        action = request.form.get("action")

        if action == "Breathing Exercise":
            bot_response = "🧘 Let's do a 2-minute deep breathing exercise. Inhale… Exhale… Repeat 5 times."
        elif action == "Motivational Quote":
            bot_response = "💡 “Believe you can and you’re halfway there.” – Theodore Roosevelt"
        else:
            # Analyze sentiment
            score = sia.polarity_scores(user_input)["compound"]

            # Determine mood and suggest response
            if score >= 0.3:
                bot_response = "😊 I'm glad to hear that! Keep up your positive energy! Maybe try a short gratitude exercise today."
            elif score <= -0.3:
                bot_response = "😔 It seems like you’re feeling low. Try a 2-minute deep breathing exercise. Would you like me to guide you?"
            else:
                bot_response = "😐 Sounds neutral. Maybe take a short break or stretch to refresh your mind."

        # Add user and bot messages to conversation
        conversation.append(("You", user_input))
        conversation.append(("Bot", bot_response))
        return redirect(url_for("chatbot"))

    # Build chat history for display
    chat_html = ""
    for speaker, msg in conversation[-10:]:  # show last 10 messages
        color = "blue" if speaker == "Bot" else "green"
        chat_html += f'<p><b style="color:{color}">{speaker}:</b> {msg}</p>'

    # Render HTML page
    return render_template_string('''
    <html>
        <head>
            <title>Mental Health Chatbot</title>
            <style>
                body {font-family: Arial; text-align: center; margin-top: 50px;}
                input[type=text] {width:300px; padding:10px;}
                input[type=submit], button {padding:10px; margin:5px;}
                .chat-box {width:400px; margin:20px auto; border:1px solid #ccc; padding:10px; height:300px; overflow-y:scroll; text-align:left;}
            </style>
        </head>
        <body>
            <h2>🧘 Mental Health Chatbot for Students</h2>
            <div class="chat-box">
                {{ chat_html|safe }}
            </div>
            <form method="POST">
                <input type="text" name="message" placeholder="How are you feeling today?" required>
                <input type="submit" value="Send">
            </form>
            <form method="POST">
                <button name="action" value="Breathing Exercise">🧘 Breathing Exercise</button>
                <button name="action" value="Motivational Quote">💡 Motivational Quote</button>
            </form>
        </body>
    </html>
    ''', chat_html=chat_html)

if __name__ == "__main__":
    app.run(debug=True)
