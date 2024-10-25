from botbuilder.core import TurnContext, ConversationState
from appointment_dialog import AppointmentDialog

class AppointmentBookingBot:
    def __init__(self, dialog: AppointmentDialog, conversation_state: ConversationState):
        self.dialog = dialog
        self.conversation_state = conversation_state
        self.dialog_state = self.conversation_state.create_property("DialogState")

    async def on_message_activity(self, turn_context: TurnContext):
        await self.dialog.run(turn_context, self.dialog_state)
        await self.conversation_state.save_changes(turn_context)
