import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


def generate_activity_image(prompt: str, output_path: str | Path) -> str:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path, override=True)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada no ficheiro .env")

    client = OpenAI(api_key=api_key)

    result = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1024x1024",
    )

    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)

    return str(output_path)