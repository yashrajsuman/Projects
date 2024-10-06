from geopy.geocoders import GoogleV3
import requests
import json
from tabulate import tabulate

def get_coordinates_from_input(input_value):
    geolocator = GoogleV3(api_key="**************************************")  # Replace with your actual API key
    location = geolocator.geocode(input_value)
    print("\nArea: ", location, "\n")
    if location:
        return f"{location.latitude},{location.longitude}"
    else:
        return None

# Replace with your Google Places API key
api_key = "AIzaSyC3_bCPrSBUEARq6et8HMZFiZkXjyTfDnI"

user_input = input("Enter your area Pincode or Location: ")

# Determine if the input is a pincode or location
if user_input.isdigit():  # Assuming pincode is numeric
    location = get_coordinates_from_input(user_input)
else:
    location = get_coordinates_from_input(user_input)

if location:
    # Search query
    query = "business"

    # Initialize a set to keep track of unique business names
    unique_business_names = set()

    # Table headers for business information
    info_table_headers = ["Business Name", "Types"]

    # Table data for business information
    info_table_data = []

    # Perform searches for each range of 100 meters
    for lower_limit in range(0, 1000, 100):
        upper_limit = min(lower_limit + 100, 1000)
        
        # Construct the URL
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={upper_limit}&type={query}&key={api_key}"

        # Send the request
        response = requests.get(url)

        # Parse the JSON response
        data = json.loads(response.text)

        # Populate the table data for business information
        for result in data.get("results", []):
            business_name = result["name"]

            # Check if the business name is unique for this iteration
            if business_name not in unique_business_names:
                business_types = result.get("types", [])
                info_table_data.append([business_name, business_types])
                unique_business_names.add(business_name)

    # Display the table for business information
    print("Business Information:")
    print(tabulate(info_table_data, headers=info_table_headers, tablefmt="pretty"))

    # Extract available business types from the data
    available_business_types = set()
    for result in data.get("results", []):
        types = result.get("types", [])
        available_business_types.update(types)

    # Get essential business types
    essential_business_types = [
        ["grocery_or_supermarket", "grocery", "supermarket"],
        ["pharmacy","health","medical"],
        ["bakery","cake shop"],
        ["hardware_store", "hardware shop"],
        ["convenience_store", "convenience shop"],
        ["laundry","wash cloth"],
        ["restaurant","restaurant","food"],
        ["barber", "hair cutting shop"],
        ["pet_store"],
        ["doctor", "medical clinic"],
        ["gym", "fitness center"],
        ["book_store", "bookshop"],
        ["market", "local market"],
        ["electronics_store", "electronics shop"],
        ["library"],
        ["bank","atm"],
        ["post_office", "post office"],
        ["school"],
        ["car_repair", "auto repair shop"],
        ["florist","flower shop"]
    ]

    # Create a table for essential business types availability
    essential_table_headers = ["Essential Business Type", "Available"]
    essential_table_data = []

    for essential_types in essential_business_types:
        is_available = any(any(word.lower() in essential_type.lower() for essential_type in essential_types) for word in available_business_types)
        essential_table_data.append([essential_types[0], "Yes" if is_available else "No"])

    # Display the table for essential business types availability
    print("\nEssential Business Types Availability:")
    print(tabulate(essential_table_data, headers=essential_table_headers, tablefmt="pretty"))
else:
    print("Invalid input or location not found.")


import pandas as pd

def read_excel_data(file_path, sheet_name):
    try:
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def print_business_info(dataframe):
    for _, row in dataframe.iterrows():
        print(f"Business Type:- {row['Business Type']}")
        print(f"Space: {row['Space']}")
        print(f"Labour: {row['Labour']}")
        print(f"Investment: {row['Investment']}")
        print(f"Skills: {row['Skills']}")
        print("\n" + "="*20 + "\n")

def main():
    # Provide the path to your Excel file
    excel_file_path =  r"C:\Users\rajy9\Downloads\Business data.xlsx"
    
    # Provide the sheet name containing the data
    sheet_name = "Sheet1"

    # Read data from Excel
    excel_data = read_excel_data(excel_file_path, sheet_name)

    if excel_data is not None:
        # Display business information
        print_business_info(excel_data)

if __name__ == "__main__":
    main()

