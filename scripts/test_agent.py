import asyncio
import base64
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src/bot"))

from agents import Runner
from llm import LLMClient
from llm.models import Draft

llm = LLMClient()

# ── test data ────────────────────────────────────────────────────────────────
SAMPLE_POST = """
Title: OpenAI releases GPT-5 with major reasoning improvements
Content: OpenAI has released GPT-5, claiming significant improvements in reasoning,
coding, and multimodal understanding. Early benchmarks show it outperforms GPT-4
on most standard tests by a wide margin.
Subreddit: artificial
Upvotes: 4200
"""

# ── helpers ──────────────────────────────────────────────────────────────────
def _get_field(obj, key):
  if isinstance(obj, dict):
    return obj.get(key)
  return getattr(obj, key, None)

def save_image(b64: str, path: str = "scripts/output.png") -> None:
  with open(path, "wb") as f:
    f.write(base64.b64decode(b64))
  print(f"✅ Image saved → {path}")


# ── tests ────────────────────────────────────────────────────────────────────
async def test_designer():
  print("\n── Designer Agent ───────────────────────────────")
  result = await Runner.run(llm.get_designer(), SAMPLE_POST)
  output = result.final_output

  for i, draft in enumerate(output.draft_options):
    print(f"\n[Option {i+1}]")
    print(f"  Intro:       {draft.intro}")
    print(f"  Bridge:      {draft.bridge}")
    print(f"  Image Draft: {draft.image_draft}")

  print(f"\nExplanation: {output.explanation}")
  return output.draft_options

async def test_artist(draft: Draft):
  print("\n── Artist Agent ─────────────────────────────────")
  prompt = f"{draft.intro}\n{draft.bridge}\n{draft.image_draft}"
  print(f"Prompt:\n{prompt}\n")

  result = await Runner.run(llm.get_artist(), prompt)
  output = result.final_output
  print(f"Image Copy:  {output.image_copy}")
  print(f"Explanation: {output.explanation}")

  for item in result.new_items:
    if _get_field(item, "type") != "tool_call_item":
      continue
    raw = _get_field(item, "raw_item")
    if _get_field(raw, "type") != "image_generation_call":
      continue
    img = _get_field(raw, "result")
    if isinstance(img, str) and img:
      save_image(img)
      break
  else:
    print("⚠️ No image returned from artist agent.")

async def test_full_flow(draft_index: int = 0):
  drafts = await test_designer()
  if not drafts:
    print("⚠️ No drafts returned.")
    return
  await test_artist(drafts[draft_index])

# ── entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description="Test LLM agents")
  parser.add_argument(
    "--mode",
    choices=["designer", "artist", "full"],
    default="full",
    help="Which agent to test (default: full)",
  )
  parser.add_argument(
    "--draft",
    type=int,
    default=0,
    help="Draft index to pass to artist (default: 0)",
  )
  parser.add_argument(
    "--topic",
    type=str,
    default=None,
    help="Override sample post with a custom topic string",
  )
  args = parser.parse_args()

  if args.topic:
    SAMPLE_POST = args.topic

  async def run():
    if args.mode == "designer":
      await test_designer()
    elif args.mode == "artist":
      drafts = await test_designer()
      if drafts:
        await test_artist(drafts[args.draft])
    else:
      await test_full_flow(draft_index=args.draft)

  asyncio.run(run())
