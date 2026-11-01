"""Check the configured provider without displaying credentials."""
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from anthropic import AsyncAnthropic, APIStatusError
from dotenv import load_dotenv

from core.llm_utils import create_message, extract_text_content


async def main():
    load_dotenv(Path(__file__).resolve().parents[1] / '.env')
    model = os.environ['ANTHROPIC_MODEL']
    async with AsyncAnthropic(
        api_key=os.environ['ANTHROPIC_API_KEY'],
        base_url=os.environ.get('ANTHROPIC_BASE_URL') or 'https://api.anthropic.com',
        timeout=30,
        max_retries=0,
    ) as client:
        try:
            response = await create_message(
                client,
                stage='configuration_check',
                model=model,
                max_tokens=32,
                messages=[{'role': 'user', 'content': '请只回复：连接成功'}],
            )
        except APIStatusError as exc:
            print(f'Model check failed: HTTP {exc.status_code}; {model}')
            raise SystemExit(1) from None
        print(f'Model: {model}')
        print(f'Stop reason: {response.stop_reason}')
        text = extract_text_content(response.content)
        print(f'Response: {text}')
        if not text or response.stop_reason != 'end_turn':
            raise SystemExit(1)


if __name__ == '__main__':
    asyncio.run(main())
