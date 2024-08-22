import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

system_prompt = '''You are an assistant that helps in summarization of calls.
You will got the call from a user and you need to summarize it following such parts:
1. What was agreed upon?
2. What was discussed?
3. Who's doing what?

Write a summarization as a plain text in a format:

Резюме

1. До чего договорились:
...

2. Что обсудили:
...

3. Кто что делает:
...
Your summarization should be obligatory written in Russian.'''


def summarize(call: str) -> str:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f'### Call ### \n{call}'}
        ]
    )

    return response.choices[0].message.content
