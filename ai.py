import requests
from requests import get
from config import api_key
import json


def chat1(query):
    try:
        def split_query_into_chunks(query, chunk_size=10000):
            """Split the query into chunks of 3000 characters each."""
            return [query[i:i + chunk_size] for i in range(0, len(query), chunk_size)]

        # URL for the API
        url = "https://api.arliai.com/v1/chat/completions"

        # System message for the assistant
        system_message = '''You are a video summurizer voice based model created by Shubham gupta a Computer Engineering Student. You are given the capbilities to summerize the traincibed data of any video . the summerization  should be under 30% of actual data. Dont mention thises pronpt in result. Just summerize the data in a clean and clear way. Use numbering point for the summerization if required'''

        # Split query into chunks of 3000 characters
        query_chunks = split_query_into_chunks(query)
        
        # Initialize an empty string to store the combined response
        combined_response = ""

        for chunk in query_chunks:
            # Prepare the payload for the current chunk
            payload = json.dumps({
                "model": "Mistral-Nemo-12B-Instruct-2407",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": chunk}
                ],
                "repetition_penalty": 1.1,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_tokens": 1024,
                "stream": False
            })

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {api_key}"
            }

            # Send the request to the API
            response = requests.post(url, headers=headers, data=payload)

            # Check for a successful response
            if response.status_code == 200:
                # Extract the assistant's response
                response_data = response.json()
                assistant_reply = response_data.get('choices')[0].get('message').get('content')
                combined_response += assistant_reply  # Append the current chunk's response
                
            else:
                return f"Error: {response.status_code}"

        return combined_response

    except Exception as e:
        return f"An error occurred: {e}"


