import requests
import os
def get_chat_response(msg_content):
    url = 'https://api.pawan.krd/v1/chat/completions'
    api=os.environ.get("OPENAI_API")
    headers = {
        'Authorization': 'Bearer ',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'gpt-3.5-turbo',
        'max_tokens': 100,
        'messages': [
            {
                'role': 'system',
                'content': 'You are an helpful assistant.'
            },
            {
                'role': 'user',
                'content': msg_content
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    
    # Return the response text
    return response.text

