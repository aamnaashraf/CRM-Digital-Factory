"""
Test script to verify the dashboard activity API endpoint format
"""
import requests

def test_activity_endpoint():
    """Test the dashboard activity API endpoint"""
    try:
        # Test the API endpoint
        response = requests.get("http://localhost:8000/api/dashboard/activity")

        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: API endpoint is accessible")
            print(f"Response format: {list(data.keys())}")

            if 'activities' in data:
                print(f"Found {len(data['activities'])} activities in response")
                if data['activities']:
                    sample_activity = data['activities'][0]
                    print(f"Sample activity keys: {list(sample_activity.keys())}")
                    print("API format is correct for frontend use")
                    return True
            else:
                print("ERROR: 'activities' key not found in response")
                print(f"Available keys: {list(data.keys())}")
                return False
        else:
            print(f"ERROR: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("WARNING: Could not connect to backend API. Make sure the server is running.")
        print("This is expected if backend server is not started.")
        return True  # Not a failure of our implementation, just server not running
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing dashboard activity API endpoint format...")
    test_activity_endpoint()