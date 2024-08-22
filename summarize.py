import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

system_prompt = ''


def summarize(call: str) -> str:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f'### Call ### \n{call}'}
        ]
    )

    return response.choices[0].message.content
