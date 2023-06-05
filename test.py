import openai
from pdfminer.high_level import extract_text
openai.api_key = ""

#Reads pdf and returns string
def extractPDF(fileName):
    text = extract_text(fileName)
    return text

text = extractPDF("big.pdf")

#Message to API
completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [{"role": "user", "content" : "How are you today?"}]
)

#Print output
print(completion.choices[0].message.content)
print(completion)
