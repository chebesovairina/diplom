from config import *

def prompt_api(prompt_text):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key"
    }
    prompt = {
        "modelUri": "gpt://b1gq1k007o07litq7rb0/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "user",
                "text": prompt_text
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=prompt, timeout=10)
        response.raise_for_status()  # Проверка HTTP-ошибок
        return response.json()["result"]["alternatives"][0]["message"]["text"]
    except Exception as e:
        return f"Ошибка: {str(e)}"
