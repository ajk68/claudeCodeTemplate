#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import json
import sys
import subprocess
import os

try:
    # Read hook input
    data = json.load(sys.stdin)
    message = data.get("message", "")

    # Different sounds for different notification types
    if "permission" in message.lower():
        # Urgent - needs your attention
        sound = "Glass"  # Sharp, attention-getting
    elif "waiting" in message.lower():
        # Claude is idle
        sound = "Ping"  # Gentle reminder
    elif "complete" in message.lower() or "finished" in message.lower():
        # Task completed
        sound = "Hero"  # Positive completion sound
    else:
        # Default notification
        sound = "Pop"  # Subtle notification

    # Play the sound
    sound_path = f"/System/Library/Sounds/{sound}.aiff"
    if os.path.exists(sound_path):
        subprocess.run(["afplay", sound_path], capture_output=True)

    # Optional: Also send to macOS notification center
    # Uncomment the following lines if you want visual notifications too
    # subprocess.run([
    #     "osascript", "-e",
    #     f'display notification "{message}" with title "Claude Code"'
    # ], capture_output=True)

except Exception:
    # Silent failure
    pass

sys.exit(0)
