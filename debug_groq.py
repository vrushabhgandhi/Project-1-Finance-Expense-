#!/usr/bin/env python3
"""Debug script to test Groq API connection."""

import os
from dotenv import load_dotenv
from groq import Groq
import json

def test_groq_connection():
    """Test basic Groq API connection and response."""
    
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    print("\n" + "="*70)
    print("🧪 GROQ API CONNECTION TEST")
    print("="*70)
    
    print(f"API Key present: {bool(api_key)}")
    print(f"Model: {model}")
    
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY not found in .env file")
        return False
    
    try:
        print("\nInitializing Groq client...")
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized successfully")
        
        print("\nSending test message...")
        message = client.chat.completions.create(
            model=model,
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Respond with valid JSON only: {\"test\": \"success\"}"
                }
            ]
        )
        
        print("✅ API call successful!")
        print(f"Response: {message.choices[0].message.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        print(f"Full error: {e}")
        return False


if __name__ == "__main__":
    success = test_groq_connection()
    print("\n" + "="*70)
    if success:
        print("✅ Groq API is working correctly!")
    else:
        print("❌ Groq API connection failed. Please check:")
        print("   1. GROQ_API_KEY is valid in .env file")
        print("   2. Internet connection is working")
        print("   3. Groq service is up (https://status.groq.com)")
    print("="*70 + "\n")
