from src.client import get_client

import anthropic

client = get_client()

INPUT_PRICE_PER_MILLION = 3
OUTPUT_PRICE_PER_MILLION = 15

total_cost = 0


system = "You're a superb coder! Who's an expert in problem solving"

messages = []

def trim_history(messages, max_tokens):
    token_count = client.messages.count_tokens(
            model = "claude-sonnet-4-6",
            messages=messages
        )
    while token_count.input_tokens > max_tokens:
        messages.pop(0)
        messages.pop(0)
        token_count = client.messages.count_tokens(
            model="claude-sonnet-4-6",
            messages=messages
        )
    return messages

while True:
    user_input=input()
    if user_input == "exit":
        break
    messages.append({"role":"user", "content": user_input})
    messages=trim_history(messages, 2000)
    token_count = client.messages.count_tokens(
        model = "claude-sonnet-4-6",
        messages=messages
    )
    print(f"Current Input tokens is : {token_count.input_tokens}")
    try:
        with client.messages.stream(
            model = "claude-sonnet-4-6",
            max_tokens = 1024,
            messages=messages,
            system=system
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
            final_message = stream.get_final_message()
            cost = (
                final_message.usage.input_tokens* INPUT_PRICE_PER_MILLION/ 1_000_000 
                + final_message.usage.output_tokens * OUTPUT_PRICE_PER_MILLION/ 1_000_000 
            )
            total_cost += cost
            print(f"Input tokens charged for this turn is : {cost} and the total cost so far is {total_cost}")
        messages.append({"role":"assistant", "content": final_message.content[0].text})
    except(anthropic.APIConnectionError):
        print("\n[Connection Lost]")
    except(anthropic.RateLimitError):
        print("\n[Rate Limit hit]")







