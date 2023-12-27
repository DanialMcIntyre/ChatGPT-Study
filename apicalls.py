from openai import OpenAI
from pdfminer.high_level import extract_text
from PyQt6 import uic, QtWidgets
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

#Reads pdf and returns string
def extractPDF(fileName):
    text = extract_text(fileName)
    return text

#Returns a summary of pdf
def summarizePDF(PDF, complexity):
    numWords = PDF.split()
    numWords = len(numWords)
    if numWords > 3000:
        print("File too large")
        return
    elif numWords > 800:
        gptModel = "gpt-3.5-turbo"
    else:
        gptModel = "gpt-3.5-turbo-16k"

    if complexity == "Brief":
        words = 100
    elif complexity == "Detailed":
        words = 200
    elif complexity == "In Depth":
        words = 300
    else:
        words = 100

    print(gptModel)
    completion = client.chat.completions.create(
    model = gptModel,
    messages = [{"role": "user", "content" : "Give a " + complexity + " summary in around " + str(words) + " of the following:\n" + PDF}]
    )
    return completion.choices[0].message.content

#Creates mock test
def createMockTest(PDF):
    numWords = PDF.split()
    numWords = len(numWords)
    print(numWords)
    if numWords > 3000:
        print("File too large")
        return
    elif numWords > 800:
        gptModel = "gpt-3.5-turbo"
    else:
        gptModel = "gpt-3.5-turbo-16k"

    completion = client.chat.completions.create(
    model = gptModel,
    messages = [{"role": "user", "content" : "Create a mock test for the following text with multiple multiple choice and short answer questions and then create an answer sheet afterwards:\n" + PDF}]
    )

    return completion.choices[0].message.content

#Creates Q-Cards
def createQCards(PDF, numCards):
    numWords = PDF.split()
    numWords = len(numWords)
    if (numWords*3 + 20*numCards) > 15000:
        print("File too large")
        return
    elif (numWords*3 + 20*numCards) > 3800:
        gptModel = "gpt-3.5-turbo"
    else:
        gptModel = "gpt-3.5-turbo-16k"

    completion = client.chat.completions.create(
    model = gptModel,
    messages = [{"role": "user", "content" : "Create " + str(numCards) + " QCards with answers in the following format: \nQuestion: Answer: \n Here is an example: \n Question: What is the main topic of the text? Answer: The main topic is about owning pets \n Do not call them anything like Q1 or A1. Simple use Question and Answer. Make the questions from the following info:\n" + PDF}]
    )

    return completion.choices[0].message.content