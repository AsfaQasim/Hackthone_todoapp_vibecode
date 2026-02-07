"""Vercel serverless function entry point"""
from mangum import Mangum
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app

# Mangum handler for Vercel
handler = Mangum(app, lifespan="off")
