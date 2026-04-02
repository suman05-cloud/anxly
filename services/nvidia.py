import os
import json
from openai import OpenAI

def stream_chat_response(messages: list):
    
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API_KEY")
    )

    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-v3.1-terminus",
        messages=messages,
        temperature=0.2,
        top_p=0.7,
        max_tokens=8192,
        extra_body={"chat_template_kwargs": {"thinking": True}},
        stream=True
    )
    
    # for streaming not to send directly
    for chunk in completion:
        if chunk.choices:
            delta = chunk.choices[0].delta.content
            if delta:
                yield f"data: {json.dumps({'chunk': delta})}\n\n"

    
    yield f"data: {json.dumps({'done': True})}\n\n"