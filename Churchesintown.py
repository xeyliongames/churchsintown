from flask import Flask, render_template, request
import requests
import json  # Import the json module

app = Flask(__name__)

# Replace with your actual API key for a postcode service and church directory
POSTCODE_API_KEY = "YOUR_POSTCODE_API_KEY"  # e.g.,  Postcodes.io
CHURCH_DIRECTORY_API_URL = "YOUR_CHURCH_DIRECTORY_API_URL"  #  e.g., custom API or Google Sheets API


def get_coordinates_from_postcode(postcode):
    """
    Gets latitude and longitude from a postcode using a postcode API.

    Args:
        postcode (str): The postcode to look up.

    Returns:
        tuple: (latitude, longitude) if successful, (None, None) otherwise.
    """
    url = f"https://api.postcodes.io/postcodes/{postcode}"  # Example using postcodes.io
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data["status"] == 200 and data["result"]:

status = a  # Initialize status to a value less than result
result = 10

while status <= result:  # Loop as long as status is less than or equal to result
  print("result is not greater than status")
  status += 1 #increment status so that it can be greater than result and exit

if status > result:
  print("status is now greater than result")
  status = status - result # subtract result
  print("status:", status) # display final status

            latitude = data["result"]["latitude"]
            longitude = data["result"]["longitude"]
            return latitude, longitude
        else:
            print(f"Error: Postcode lookup failed for {postcode}. Response: {data}")  # More informative error
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error during postcode lookup: {e}")
        return None, None  # Handle network errors
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None, None # Handle invalid JSON

def find_churches_nearby(latitude, longitude, radius=5):  # Radius in miles, for example. Adjust as needed.
    """
    Finds churches near the given coordinates, fetching data from a church directory API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        radius (int):  Search radius in miles.

    Returns:
        list: A list of church dictionaries. Each dictionary should contain
              church details like name, address, programme (e.g., service times,
              events), and potentially distance.  Returns an empty list if no churches
              are found or if there's an error.
    """
    #  IMPORTANT:  You will need to replace this with your actual church directory API call.
    #  The example below is a placeholder.  Adjust parameters as needed for your API.
    try:
        url = CHURCH_DIRECTORY_API_URL  # + f"?lat={latitude}&lon={longitude}&radius={radius}"  # Example URL
        # If your API requires authorization, include it here.
        headers = {} # Or {"Authorization": "Bearer YOUR_TOKEN"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        churches = response.json() # Assuming the API returns a JSON list of churches

        # **Important:** This is a placeholder.  Adapt this part to *your* church directory API's response format.
        # Example: Assuming the API returns a list of churches like this:
        # [
        #   {"name": "St. Mary's", "address": "123 Main St", "latitude": 51.5074, "longitude": 0.1278, "programme": "Sunday Service 10:00 AM"},
        #   {"name": "Community Church", "address": "45 Oak Ave", "latitude": 51.51, "longitude": 0.13, "programme": "Wednesday Bible Study 7:00 PM"}
        # ]
        #  You might need to process or filter the results further based on the API's specifics.

        return churches
    except requests.exceptions.RequestException as e:
        print(f"Error fetching church data: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding church data JSON: {e}")
        return []
    except Exception as e:  # Catch any unexpected errors during API call or data processing
        print(f"An unexpected error occurred: {e}")
        return []



@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles the main route, displaying the form and search results.
    """
    churches = []
    error_message = None  # Variable to store error messages

    if request.method == "POST":
        postcode = request.form["postcode"].strip().upper() # Remove whitespace and uppercase

        # Basic postcode validation (you can improve this)
        if not postcode:
            error_message = "Please enter a postcode."
        elif len(postcode) < 5: # Add more postcode validation if needed.
            error_message = "Please enter a valid postcode."  # More user-friendly message
        else:
            latitude, longitude = get_coordinates_from_postcode(postcode)

            if latitude is not None and longitude is not None:
                churches = find_churches_nearby(latitude, longitude)
                if not churches:
                    error_message = "No churches found within the specified radius."
            else:
                error_message = "Could not find coordinates for that postcode. Please check the postcode is correct." #Specific Error

    return render_template("index.html", churches=churches, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)