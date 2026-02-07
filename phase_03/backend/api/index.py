"""Vercel serverless function entry point"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app

# Export for Vercel
handler = app
