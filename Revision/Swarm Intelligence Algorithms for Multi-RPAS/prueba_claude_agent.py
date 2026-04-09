import asyncio
import os
import sys
import io
from typing import Any
from dotenv import load_dotenv

# Configurar la terminal para manejar UTF-8 (evita errores en Windows)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    create_sdk_mcp_server,
    tool,
)
from langsmith.integrations.claude_agent_sdk import configure_claude_agent_sdk

# Configurar el rastreo de LangSmith para el SDK de agentes de Claude
configure_claude_agent_sdk()


@tool(
    "get_weather",
    "Gets the current weather for a given city",
    {"city": str},
)
async def get_weather(args: dict[str, Any]) -> dict[str, Any]:
    city = args["city"]
    weather_data = {
        "San Francisco": "Foggy, 62°F",
        "New York": "Sunny, 75°F",
        "London": "Rainy, 55°F",
        "Tokyo": "Clear, 68°F",
    }
    weather = weather_data.get(city, "Weather data not available")
    return {"content": [{"type": "text", "text": f"Weather in {city}: {weather}"}]}


async def main() -> None:
    weather_server = create_sdk_mcp_server(
        name="weather",
        version="1.0.0",
        tools=[get_weather],
    )

    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",
        system_prompt="You are a friendly travel assistant who helps with weather information.",
        mcp_servers={"weather": weather_server},
        allowed_tools=["mcp__weather__get_weather"],
    )

    print("\n" + "=" * 60)
    print("INICIANDO CLAUDE AGENT SDK CON LANGSMITH TRACING")
    print("=" * 60)

    async with ClaudeSDKClient(options=options) as client:
        print("\n[PREGUNTA]: What's the weather like in San Francisco and Tokyo?\n")
        await client.query("What's the weather like in San Francisco and Tokyo?")

        async for message in client.receive_response():
            # El mensaje suele ser un objeto con información del agente y la respuesta
            print(f"[MENSAJE]: {message}")


if __name__ == "__main__":
    asyncio.run(main())
