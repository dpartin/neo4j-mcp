#!/usr/bin/env python3
"""
Simple test to check basic functionality
"""

print("Starting simple test...")

# Test 1: Basic imports
try:
    import os
    print("✅ os imported")
except Exception as e:
    print(f"❌ os import failed: {e}")

try:
    import logging
    print("✅ logging imported")
except Exception as e:
    print(f"❌ logging import failed: {e}")

try:
    from typing import Optional, Dict, Any, List
    print("✅ typing imported")
except Exception as e:
    print(f"❌ typing import failed: {e}")

# Test 2: Check if .env exists
try:
    if os.path.exists(".env"):
        print("✅ .env file exists")
    else:
        print("❌ .env file missing")
except Exception as e:
    print(f"❌ Error checking .env: {e}")

# Test 3: Try to import server
try:
    import server
    print("✅ server imported successfully")
except Exception as e:
    print(f"❌ server import failed: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.")
