import os
import json
import requests
from requests.exceptions import RequestException
from prompts import llama
from config.settings import SECRET_AI_API_URL

api_key = os.environ.get("SECRET_AI_API_KEY", "N/A")

def process_id_image(id_image):
    """
    Process an ID image with SecretAI Vision to extract identity information
    
    Args:
        id_image (str): Base64-encoded image string
        
    Returns:
        dict: Results of ID verification including identity data and fake detection
    """

    
    messages = [
        {"role": "system", "content": llama.ID_DETECTION_PROMPT},
        {
            "role": "user", 
            "content": "Analyze this ID image to extract identity data and detect fakes:",
            "images": [id_image]
        }
    ]
    
    try:
        print(f"Sending image to SecretAI: {id_image[:50]}...")
        
        # This is a placeholder implementation until a proper SecretAI Python SDK is available
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3.2-vision",
            "messages": messages,
            "temperature": 1
        }
        
        response = requests.post(
            SECRET_AI_API_URL,
            headers=headers,
            json=payload,
            timeout=5
        )
        
        if response.status_code != 200:
            raise Exception(f"SecretAI API error: {response.status_code} - {response.text}")
            
        response_data = response.json()
        print(f"Raw SecretAI response: {json.dumps(response_data, indent=2)}")
        
        # Extract content from response (structure might need adjustment based on actual SecretAI Python SDK)
        content = response_data.get("message", {}).get("content") or response_data.get("content")
        
        try:
            # Try to parse the JSON result
            result = json.loads(content)
        except json.JSONDecodeError:
            # Fallback: Extract JSON from potential markdown or text wrapper
            import re
            json_match = re.search(r'{[\s\S]*}', content)
            if json_match:
                result = json.loads(json_match.group(0))
            else:
                raise Exception("No valid JSON found in response")
        
        # Validate response structure
        if not result.get("success") or "identity" not in result or "is_fake" not in result:
            raise Exception("Invalid response structure from SecretAI Vision")
            
        return {
            "response": response_data,
            "success": result.get("success"),
            "identity": result.get("identity"),
            "is_fake": result.get("is_fake"),
            "fake_reason": result.get("fake_reason")
        }
        
    except RequestException as e:
        print(f"SecretAI Vision network error: {str(e)}")
        return {
            "response": None,
            "success": False,
            "identity": {
                "country": "",
                "id_number": "",
                "name": "",
                "date_of_birth": 0,
                "document_expiration": 0
            },
            "is_fake": True,
            "fake_reason": f"Network error while processing image: {str(e)}"
        }
    except Exception as e:
        print(f"SecretAI Vision error: {str(e)}")
        print(f"Full error object: {json.dumps(str(e), indent=2)}")
        return {
            "response": None,
            "success": False,
            "identity": {
                "country": "",
                "id_number": "",
                "name": "",
                "date_of_birth": 0,
                "document_expiration": 0
            },
            "is_fake": True,
            "fake_reason": f"Failed to process image: {str(e)}"
        }