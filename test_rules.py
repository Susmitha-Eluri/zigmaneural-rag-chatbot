import requests
import json

def test_query(question):
    url = "http://localhost:8010/ask"
    payload = {"question": question}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"\nQuestion: {question}")
        print(f"Answer: {data['answer']}")
        print(f"Length (words): {len(data['answer'].split())}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Test cases
    print("--- Running Verification Tests ---")
    
    # 1. Simple factual question (3-5 sentences)
    test_query("What is Zigma Neutral?")
    
    # 2. Descriptive question (100-150 words)
    test_query("Explain the remote work policy.")
    
    # 3. Policy-related question (structured explanation)
    test_query("Tell me about the health benefits.")
