import json
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

try:
    print("Testing step-3.5-flash...")
    start = time.time()
    completion = client.chat.completions.create(
      model="stepfun-ai/step-3.5-flash",
      messages=[{"role":"user","content":"Generate exactly a JSON array with one item. [{\"a\": 1}]"}],
      temperature=0.3,
      top_p=0.95,
      max_tokens=40,
      extra_body={"chat_template_kwargs":{"thinking":False}},
      stream=False,
      timeout=15
    )
    print("SUCCESS")
    print(repr(completion.choices[0].message.content))
    print("\n\nTime taken:", time.time() - start)
except Exception as e:
    print("Error with v4-flash:", e)

try:
    print("\nTesting v3.2...")
    start = time.time()
    completion = client.chat.completions.create(
      model="deepseek-ai/deepseek-v3.2",
      messages=[{"role":"user","content":"Generate exactly a JSON array with one item. [{\"a\": 1}]"}],
      temperature=0.3,
      top_p=0.95,
      max_tokens=40,
      extra_body={"chat_template_kwargs":{"thinking":False}},
      stream=False,
      timeout=15
    )
    print("SUCCESS")
    print(repr(completion.choices[0].message.content))
    print("\n\nTime taken:", time.time() - start)
except Exception as e:
    print("Error with v3.2:", e)
