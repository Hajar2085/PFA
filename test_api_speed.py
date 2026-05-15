import json
from openai import OpenAI
import time

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
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

