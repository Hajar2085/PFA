import json
from openai import OpenAI
import time

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
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
