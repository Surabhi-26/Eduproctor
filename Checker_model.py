
import google_auth_oauthlib
import google_auth_httplib2
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

GOOGLE_API_KEY="API_KEY"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
question="What is LIFO?"
answer="Last in first out"
response = model.generate_content(f"question={question} and answer={answer} so just give me true or false")
print(response.text)