import os
import pypdf
from langgraph.graph import StateGraph
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

def test_swarm_readiness():
    load_dotenv()
    print("🛠️  STARTING FORENSIC READINESS CHECK...\n")
    
    # 1. Test Environment Variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ FAIL: OPENAI_API_KEY not found in .env")
        return
    print("✅ PASS: Environment Variables Loaded.")

    # 2. Test PDF Library
    try:
        ver = pypdf.__version__
        print(f"✅ PASS: PyPDF Library operational (v{ver}).")
    except Exception as e:
        print(f"❌ FAIL: PyPDF Library issue: {e}")

    # 3. Test LLM Connection (Modern Invoke Syntax)
    try:
        llm = ChatOpenAI(model="gpt-4o")
        # Modern LangChain uses .invoke()
        response = llm.invoke("Respond with the word 'Ready' and nothing else.")
        if "Ready" in response.content:
            print("✅ PASS: OpenAI Connection Verified.")
    except Exception as e:
        print(f"❌ FAIL: LLM Connection: {e}")

    print("\n🏛️  REAL CONCLUSION: If all PASS, you are officially ready.")

if __name__ == "__main__":
    test_swarm_readiness()