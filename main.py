import os
from guardrails import Guard, docs_utils
from guardrails.errors import ValidationError
from rich import print
from guardrails.hub import ProfanityFree, ToxicLanguage
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

# Read the PDF document
try:
    content = docs_utils.read_pdf("./data/chase_card_agreement.pdf")
    print(f"Chase Credit Card Document:\n\n{content[:275]}\n...")
except Exception as e:
    print(f"[red]Error reading PDF:[/red] {e}")
    content = ""

def main():
    guard = Guard()
    guard.name = 'ChatBotGuard'
    guard.use_many(ProfanityFree(), ToxicLanguage())

    base_message ={
        "role": "system",
        "content": """You are a helpful assistant. 

        Use the document provided to answer the user's question. 

        ${document}
        """
    }

    def history_to_messages(history):
        messages = [base_message]
        for message in history:
            messages.append({"role": "user", "content": message[0]})
            messages.append({"role": "assistant", "content": message[1]})
        return messages

    def random_response(message, history):
        messages = history_to_messages(history)
        messages.append({"role": "user", "content": message})
        try:
            response = guard(
                model="gpt-4o",
                messages=messages,
                prompt_params={"document": content[:6000]},
                temperature=0,
            )
        except Exception as e:
            if isinstance(e, ValidationError):
                return "I'm sorry, I can't answer that question."
            return f"I'm sorry there was a problem, I can't answer that question.\nError: {e}"
        return response.validated_output

    gr.ChatInterface(random_response).launch()

if __name__ == "__main__":
    main()