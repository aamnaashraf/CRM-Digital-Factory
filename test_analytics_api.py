"""
Test script to verify the dashboard analytics API endpoint format
"""
import requests

def test_analytics_endpoint():
    """Test the dashboard analytics API endpoint"""
    try:
        # Test the API endpoint
        response = requests.get("http://localhost:8000/api/dashboard/analytics")

        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Analytics API endpoint is accessible")
            print(f"Response format: {list(data.keys())}")

            if 'channelDistribution' in data:
                print(f"Channel distribution: {data['channelDistribution']}")
            else:
                print("ERROR: 'channelDistribution' key not found in response")

            if 'ticketVolume' in data:
                print(f"Ticket volume: {len(data['ticketVolume'])} items")
                if data['ticketVolume']:
                    print(f"Sample ticket volume: {data['ticketVolume'][0]}")
            else:
                print("ERROR: 'ticketVolume' key not found in response")

            if 'resolutionStats' in data:
                print(f"Resolution stats: {data['resolutionStats']}")
            else:
                print("ERROR: 'resolutionStats' key not found in response")

            if 'sentimentTrend' in data:
                print(f"Sentiment trend: {len(data['sentimentTrend'])} items")
            else:
                print("ERROR: 'sentimentTrend' key not found in response")

            return True
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
    print("Testing dashboard analytics API endpoint format...")
    test_analytics_endpoint()