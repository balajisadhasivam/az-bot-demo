from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnStatus, DialogSet
from botbuilder.dialogs.prompts import TextPrompt, ChoicePrompt, PromptOptions
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory

class AppointmentDialog(ComponentDialog):
    def __init__(self):
        super(AppointmentDialog, self).__init__(AppointmentDialog.__name__)

        self.add_dialog(TextPrompt("TextPrompt"))
        self.add_dialog(ChoicePrompt("ChoicePrompt"))

        # Waterfall steps
        self.add_dialog(WaterfallDialog("WaterfallDialog", [
            self.ask_name_step,
            self.ask_phone_step,
            self.ask_email_step,
            self.ask_specialty_step,
            self.ask_gender_step,
            self.ask_doctor_step,
            self.ask_datetime_step,
            self.confirm_booking_step
        ]))

        self.initial_dialog_id = "WaterfallDialog"

    async def ask_name_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Please enter your name:")))

    async def ask_phone_step(self, step_context: WaterfallStepContext):
        step_context.values["name"] = step_context.result
        return await step_context.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Please enter your phone number:")))

    async def ask_email_step(self, step_context: WaterfallStepContext):
        step_context.values["phone"] = step_context.result
        return await step_context.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Please enter your email address:")))

    async def ask_specialty_step(self, step_context: WaterfallStepContext):
        step_context.values["email"] = step_context.result
        return await step_context.prompt("ChoicePrompt", PromptOptions(
            prompt=MessageFactory.text("Please choose a specialty:"),
            choices=[Choice("Cardiology"), Choice("Dermatology"), Choice("Pediatrics")]
        ))

    async def ask_gender_step(self, step_context: WaterfallStepContext):
        step_context.values["specialty"] = step_context.result.value
        return await step_context.prompt("ChoicePrompt", PromptOptions(
            prompt=MessageFactory.text("Do you prefer a male or female doctor?"),
            choices=[Choice("Male"), Choice("Female")]
        ))

    async def ask_doctor_step(self, step_context: WaterfallStepContext):
        step_context.values["gender"] = step_context.result.value
        return await step_context.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Please enter the doctor's name:")))

    async def ask_datetime_step(self, step_context: WaterfallStepContext):
        step_context.values["doctor"] = step_context.result
        return await step_context.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Please enter your preferred date and time:")))

    async def confirm_booking_step(self, step_context: WaterfallStepContext):
        step_context.values["datetime"] = step_context.result

        # Confirm appointment details
        name = step_context.values["name"]
        phone = step_context.values["phone"]
        email = step_context.values["email"]
        specialty = step_context.values["specialty"]
        gender = step_context.values["gender"]
        doctor = step_context.values["doctor"]
        datetime = step_context.values["datetime"]

        confirmation_message = (
            f"Booking confirmed! Here are the details:\n\n"
            f"- Name: {name}\n"
            f"- Phone: {phone}\n"
            f"- Email: {email}\n"
            f"- Specialty: {specialty}\n"
            f"- Doctor: {gender} - {doctor}\n"
            f"- Date and Time: {datetime}\n"
        )

        await step_context.context.send_activity(MessageFactory.text(confirmation_message))
        return await step_context.end_dialog()

    async def run(self, turn_context, accessor):
        dialog_set = DialogSet(accessor)
        dialog_set.add(self)

        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()

        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(self.id)
