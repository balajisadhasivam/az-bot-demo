import os
import asyncio
from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, ConversationState, MemoryStorage
from botbuilder.schema import Activity
from appointment_dialog import AppointmentDialog
from bot import AppointmentBookingBot

app = Flask(__name__)

# Fetch App ID and Password from environment variables
app_id = os.getenv("MicrosoftAppId", "92c28de8-2339-40bc-a747-c1339f0f01bb")
app_password = os.getenv("MicrosoftAppPassword", "i2R8Q~WArtpNaAslwVTwp5S1Cxy22oyF6jHTMdB8")

# Adapter configuration with the App ID and Password
adapter_settings = BotFrameworkAdapterSettings(app_id, app_password)
adapter = BotFrameworkAdapter(adapter_settings)

# In-memory storage and state setup
memory = MemoryStorage()
conversation_state = ConversationState(memory)
dialog = AppointmentDialog()

# Initialize the bot with both dialog and conversation state
bot = AppointmentBookingBot(dialog, conversation_state)

@app.route("/api/messages", methods=["POST"])
def messages():
    body = request.get_json()
    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")
    response = asyncio.run(adapter.process_activity(activity, auth_header, bot.on_message_activity))
    return response or Response(status=200)

if __name__ == "__main__":
    app.run(port=3978)
