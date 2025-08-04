import requests
import base64
import os

API_KEY = "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"
image_path = "/Users/santoshr/Downloads/dc vs lsg.webp"  # Change to your image path

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")

# Encode image
base64_img = encode_image_to_base64(image_path)
data_url = f"data:image/jpeg;base64,{base64_img}"

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image."},
            {
                "type": "image_url",
                "image_url": {
                    "url": data_url
                }
            }
        ]
    }
]

payload = {
    "model": "openai/gpt-4o-mini",
    "messages": messages
}

response = requests.post(url, headers=headers, json=payload)

# Print response
if response.status_code == 200:
    data = response.json()
    result = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    print("🧠 Model Response:")
    print(result)
else:
    print(f"❌ Error {response.status_code}: {response.text}")
