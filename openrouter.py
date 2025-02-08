from openai import OpenAI
from os import getenv
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

# Free limit: If you are using a free model variant (with an ID ending in :free), then you will be limited to 20 requests per minute and 200 requests per day.

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=getenv("OPENROUTER_API_KEY"),
)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate(image_path):
    image = encode_image(image_path)
    completion = client.chat.completions.create(
        model="meta-llama/llama-3.2-11b-vision-instruct:free",
        messages=[{
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": "Describe the person in the picture by stating the following characteristics in the given structure:\nApproximate Age:\nSex/Gender:\nRace/Ethnicity:\nBuild:\nComplexion:\nEye Color:\nHair Color and Style:"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image}"
            }}]
        }])
    # print(completion)
    return completion.choices[0].message.content

if __name__ == "__main__":
    image_path = "person.jpg"
    print(generate(image_path))