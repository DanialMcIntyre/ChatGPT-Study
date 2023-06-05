import openai
from pdfminer.high_level import extract_text
openai.api_key = "api"

def extractPDF(fileName):
    text = extract_text(fileName)
    return text

text = extractPDF("big.pdf")



completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [{"role": "user", "content" : "Create a 800 word summary as well as 10 questions with answers: \n" + text}]
)

print(completion.choices[0].message.content)
print(completion)