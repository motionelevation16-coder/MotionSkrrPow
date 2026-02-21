#!/usr/bin/env python3
"""
LinkedIn Outreach Helper
========================

This script helps personalize LinkedIn connection requests and messages.
It uses free AI (Gemini or Groq) to generate personalized messages.

Usage:
    python linkedin_outreach.py --profile "URL or description" --type "connection|message"
    
Or use the interactive mode:
    python linkedin_outreach.py
"""

import os
import json
import argparse
from datetime import datetime

# Try to import AI libraries (fall back gracefully)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# ============================================
# CONFIGURATION
# ============================================

# Your value proposition (customize this)
VALUE_PROP = """
We build automations that save businesses 20+ hours/week on repetitive tasks.
Email management, social media posting, lead follow-ups, data entry — all on autopilot.
Most clients see ROI in the first week.
"""

# Connection request templates (max 300 chars on LinkedIn)
CONNECTION_TEMPLATES = [
    "Hey {first_name} — saw your work on {hook}. I help {industry} businesses automate repetitive tasks. Would love to connect!",
    "Hi {first_name}! Fellow {shared_interest} here. Building something in the automation space — thought we might have synergies. Connect?",
    "Hey {first_name}, came across your profile while researching {industry}. Impressed by {hook}. Would love to be in your network.",
]

# Message templates (for existing connections)
MESSAGE_TEMPLATES = [
    """Hey {first_name}!

Hope you're doing well. Quick question:

What's the most time-consuming repetitive task in your business right now?

Asking because I've been helping {industry} businesses automate stuff like {example_tasks} — usually saves 10-20 hrs/week.

Worth a quick chat?""",

    """Hi {first_name},

Saw your recent post about {recent_activity}. Really resonated.

Random question: Have you explored automating any of your workflows? 

I've been building automation systems for {industry} businesses and curious if that's on your radar.

No pitch — just genuinely curious about your setup.""",
]

# ============================================
# AI PERSONALIZATION
# ============================================

def get_ai_client():
    """Get available AI client"""
    if GEMINI_AVAILABLE and os.getenv("GEMINI_API_KEY"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        return "gemini"
    elif GROQ_AVAILABLE and os.getenv("GROQ_API_KEY"):
        return "groq"
    else:
        return None

def generate_with_gemini(prompt: str) -> str:
    """Generate text with Gemini (free tier)"""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def generate_with_groq(prompt: str) -> str:
    """Generate text with Groq (free tier)"""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def personalize_message(profile_info: str, message_type: str = "connection") -> str:
    """Generate personalized message using AI"""
    
    ai_client = get_ai_client()
    
    if message_type == "connection":
        char_limit = "300 characters MAX (LinkedIn limit)"
        templates = CONNECTION_TEMPLATES
    else:
        char_limit = "500 characters ideal, max 1000"
        templates = MESSAGE_TEMPLATES
    
    prompt = f"""
You are helping write a LinkedIn {message_type} message.

TARGET PROFILE:
{profile_info}

YOUR VALUE PROPOSITION:
{VALUE_PROP}

EXAMPLE TEMPLATES:
{json.dumps(templates, indent=2)}

RULES:
- {char_limit}
- Be conversational, not salesy
- Find something specific to mention (their work, posts, company)
- Don't be generic — personalize to THIS person
- No emojis in connection requests
- End with a soft CTA (connect, chat) not a hard sell
- Sound like a human, not a bot

Write the message. Return ONLY the message text, nothing else.
"""
    
    if ai_client == "gemini":
        return generate_with_gemini(prompt)
    elif ai_client == "groq":
        return generate_with_groq(prompt)
    else:
        # Fallback: simple template fill
        print("\n⚠️  No AI API configured. Using template fallback.")
        print("Set GEMINI_API_KEY or GROQ_API_KEY for AI personalization.\n")
        
        template = templates[0]
        return template.format(
            first_name="[Name]",
            hook="[specific thing you noticed]",
            industry="[their industry]",
            shared_interest="[shared interest]",
            example_tasks="email, scheduling, data entry",
            recent_activity="[recent post/activity]"
        )

# ============================================
# TRACKING
# ============================================

def log_outreach(profile: str, message: str, message_type: str):
    """Log outreach to CSV for tracking"""
    log_file = "linkedin_outreach_log.csv"
    
    # Create file with headers if doesn't exist
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("timestamp,type,profile,message,sent,response\n")
    
    # Append entry
    timestamp = datetime.now().isoformat()
    with open(log_file, "a") as f:
        # Escape quotes in message
        safe_message = message.replace('"', '""')
        safe_profile = profile.replace('"', '""')
        f.write(f'"{timestamp}","{message_type}","{safe_profile}","{safe_message}","pending",""\n')
    
    print(f"📝 Logged to {log_file}")

# ============================================
# MAIN
# ============================================

def interactive_mode():
    """Interactive outreach helper"""
    print("\n" + "="*50)
    print("🔗 LinkedIn Outreach Helper")
    print("="*50)
    
    print("\nMessage type:")
    print("1. Connection request (300 char limit)")
    print("2. Message to existing connection")
    
    type_choice = input("\nChoice (1/2): ").strip()
    message_type = "connection" if type_choice == "1" else "message"
    
    print("\nPaste profile info (name, title, company, recent posts, etc.):")
    print("(Enter a blank line when done)")
    
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    profile_info = "\n".join(lines)
    
    if not profile_info.strip():
        print("No profile info provided. Exiting.")
        return
    
    print("\n⏳ Generating personalized message...\n")
    
    message = personalize_message(profile_info, message_type)
    
    print("="*50)
    print("📨 YOUR MESSAGE:")
    print("="*50)
    print()
    print(message)
    print()
    print(f"📏 Length: {len(message)} characters")
    print("="*50)
    
    # Offer to log
    log_choice = input("\nLog this outreach? (y/n): ").strip().lower()
    if log_choice == "y":
        log_outreach(profile_info[:100], message, message_type)
    
    # Offer to continue
    continue_choice = input("\nGenerate another? (y/n): ").strip().lower()
    if continue_choice == "y":
        interactive_mode()

def main():
    parser = argparse.ArgumentParser(description="LinkedIn Outreach Helper")
    parser.add_argument("--profile", "-p", help="Profile info or URL")
    parser.add_argument("--type", "-t", choices=["connection", "message"], 
                       default="connection", help="Message type")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive or not args.profile:
        interactive_mode()
    else:
        message = personalize_message(args.profile, args.type)
        print(message)

if __name__ == "__main__":
    main()
