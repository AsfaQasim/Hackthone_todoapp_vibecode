#!/usr/bin/env python3
"""
Test with environment variable set directly
"""
import os
import sys

# Set the OpenAI API key directly
#  api key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_with_env():
    print("🔧 Testing with environment variable set directly")
    print("=" * 60)
    
    try:
        from src.config import settings
        print(f"OpenAI API key: {settings.openai_api_key[:10]}...")
        
        if not settings.openai_api_key:
            print("❌ Still no API key")
            return False
            
        print("✅ API key loaded successfully")
        
        # Now test ChatAgent
        from src.agents.chat_agent import ChatAgent
        from src.db import get_db
        from sqlmodel import select
        from src.models.base_models import User
        import uuid
        
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        
        # Get existing test user
        stmt = select(User).where(User.email == "test@example.com")
        test_user = db.exec(stmt).first()
        
        if not test_user:
            print("❌ No test user found")
            return False
            
        print(f"✅ Test user: {test_user.id}")
        
        # Create ChatAgent
        chat_agent = ChatAgent(db, test_user)
        print("✅ ChatAgent created")
        
        # Test message processing
        print("\n🧪 Testing message processing...")
        
        test_message = "Add a task: 'Environment fix test task'"
        conversation_id = str(uuid.uuid4())
        
        print(f"📤 Sending message: {test_message}")
        
        result = chat_agent.process_message(test_message, conversation_id)
        
        print(f"\n📊 ChatAgent result:")
        print(f"   Response: {result.get('response', 'No response')}")
        print(f"   Tool calls: {len(result.get('tool_calls', []))}")
        print(f"   Error: {result.get('error', 'None')}")
        
        if result.get('tool_calls'):
            for i, tool_call in enumerate(result['tool_calls']):
                print(f"   Tool {i+1}: {tool_call.get('tool_name')} - Success: {tool_call.get('result', {}).get('success', False)}")
                if not tool_call.get('result', {}).get('success', False):
                    print(f"      Error: {tool_call.get('result', {}).get('error', 'Unknown')}")
        
        # Check if any tool calls were successful
        successful_tools = [tc for tc in result.get('tool_calls', []) if tc.get('result', {}).get('success', False)]
        
        if successful_tools:
            print("🎉 ChatAgent is working correctly!")
            return True
        else:
            print("❌ ChatAgent tool calls failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_with_env()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Environment fix worked!")
    else:
        print("❌ Still needs investigation")