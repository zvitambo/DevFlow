
from agents import Agent, Runner
from infrastructure.appsettings import settings
from ..tools.mathematical_tools import (
    compute_exponential,
    compute_factorial,
    compute_fibonacci,
)


# Verify API key is loaded
api_key = settings.openai_api_key
if not api_key:
    print("⚠️ Warning: OPENAI_API_KEY not found")
else:
    print("✓ OpenAI API key loaded successfully")


# Create the agent with the mathematical tools
agent = Agent(
    name="Numeric Computation Agent",
    instructions=(
        "You are a numeric computation specialist. You can calculate factorial, "
        "exponential (power), and Fibonacci numbers. "
        "When the user asks for any of these computations, use the appropriate tool. "
        "For factorial, use `compute_factorial`. "
        "For exponential (power), use `compute_exponential`. "
        "For Fibonacci, use `compute_fibonacci`. "
        "If the user asks about anything else, politely inform them that your expertise "
        "is limited to these numeric computations."
    ),
    model="gpt-5-mini",  # You can also use other models
    tools=[compute_factorial, compute_exponential, compute_fibonacci],
)

print("✓ Agent initialized successfully")

async def run_agent():
    #. query = "Compute the factorial of 50"
    # Test multiple computations in one query
    query = "Calculate the factorial of 7 and also tell me what is 3 to the power of 4"
    print(f"📝 Query: {query}")
    print("=" * 60)

    result = await Runner.run(agent, input=query)

    print("=" * 60)
    print(f"🤖 Agent Response:")
    print(result.final_output)

