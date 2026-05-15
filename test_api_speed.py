import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent / '.env')

api_key = os.environ.get('NVIDIA_API_KEY')
if not api_key:
    raise SystemExit('Définissez NVIDIA_API_KEY dans le fichier .env')

client = OpenAI(
    base_url=os.environ.get('NVIDIA_API_BASE_URL', 'https://integrate.api.nvidia.com/v1'),
    api_key=api_key,
)

def test_model(model_name):
    print(f"Testing {model_name}...")
    try:
        start = time.time()
        completion = client.chat.completions.create(
          model=model_name,
          messages=[{"role":"user","content":"Hello, respond with 'OK' only."}],
          max_tokens=10,
          stream=False,
          timeout=30
        )
        print(f"SUCCESS: {completion.choices[0].message.content}")
        print(f"Time: {time.time() - start:.2f}s")
    except Exception as e:
        print(f"FAILED: {e}")

test_model("stepfun-ai/step-3.5-flash")
test_model("deepseek-ai/deepseek-v4-flash")
test_model("deepseek-ai/deepseek-v4-pro")
