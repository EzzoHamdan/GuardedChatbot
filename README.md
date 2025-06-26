# GuardedChatbot

A simple chatbot demo using Guardrails for moderation and Gradio for the user interface.  
It answers questions using information extracted from a PDF document.

## Usage

1. Clone the repo.
2. Install requirements: `pip install -r requirements.txt`
3. Add your PDF document to the 'data' folder
4. In main.py, update the filename in the line `content = docs_utils.read_pdf("./data/chase_card_agreement.pdf")` to match your document's name
5. Run: `python main.py`