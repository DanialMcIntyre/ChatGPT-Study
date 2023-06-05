import openai

openai.api_key = "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"

completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [{"role": "user", "content" : "Hi!"}]
)

print(completion)