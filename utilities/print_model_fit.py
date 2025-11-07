"""
Reusable utility for printing model fit summary based on character count.
"""

def print_model_fit_summary(total_chars):
    """
    Prints a summary of whether the content fits within various LLM context windows.
    
    Args:
        total_chars: Total number of characters in the content
    """
    est_tokens = total_chars // 4
    
    within = lambda limit: "✅ within" if est_tokens < limit else "❌ exceeds"
    
    print("\nModel fit summary:")
    print(f"OpenAI GPT-4o/GPT-5: {within(128_000)}")
    print(f"Claude 3.5 Sonnet:    {within(200_000)}")
    print(f"Gemini 1.5 Pro:       {within(1_000_000)}")
    print(f"Grok-2:               {within(128_000)}")
    print(f"Meta LLaMA 3.1:       {within(128_000)}")