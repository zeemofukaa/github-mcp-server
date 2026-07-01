import re
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text

        # Remove Markdown bold
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

        # Remove Markdown italics
        text = re.sub(r"\*(.*?)\*", r"\1", text)

        return text

    except Exception as e:

        error = str(e)

        if "429" in error:
            return (
                "[ERROR] Gemini API quota exceeded.\n\n"
                "Please wait a minute and try again."
            )

        elif "503" in error:
            return (
                "[ERROR] Gemini API temporarily unavailable.\n\n"
                "Google's servers are experiencing high demand.\n"
                "Please try again in a few minutes."
        )

        else:
            return (
                "[ERROR] Unable to contact Gemini.\n\n"
                f"{error}"
            )