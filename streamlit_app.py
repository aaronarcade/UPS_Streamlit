import streamlit as st
from ups_auth import get_ups_token
from ups_api import get_ups_shipping_rate, get_ups_estimated_delivery
from datetime import datetime

# Load secrets
client_id = st.secrets["ups_api"]["client_id"]
client_secret = st.secrets["ups_api"]["client_secret"]

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

# Get the access token at app startup
try:
    access_token = get_ups_token(client_id, client_secret)
except Exception as e:
    st.error(f"Failed to authenticate with UPS API: {str(e)}")
    st.stop()

# Set up the sidebar
st.sidebar.title("Options")

# Check if access_token is in session state
if st.session_state["access_token"]:
    st.sidebar.success("You're authorized with UPS.")
else:
    st.sidebar.error("Go to UPS OAuth to get authorized.")

# Create a dropdown menu in the sidebar
option = st.sidebar.selectbox(
    "Choose an option:",
    ("UPS OAuth", "Estimated Price", "Estimated Delivery", "Coming Soon...")
)

# Display the selected option
st.write(f"You selected: {option}")

# Add logic for each option
if option == "Estimated Price":
    # Define a mapping of addresses to their components
    address_mapping = {
        "211 Longview Ave. Unit 309 Celebration, FL": {
            "City": "Celebration",
            "StateProvinceCode": "FL",
            "CountryCode": "US",
            "PostalCode": "34747"
        },
        "17757 Front Beach Rd. Unit 1809 Panama City Beach, FL 32413": {
            "City": "Panama City Beach",
            "StateProvinceCode": "FL",
            "CountryCode": "US",
            "PostalCode": "32413"
        },
        "37th St NW & O St NW Office 302 Washington, DC 20057": {
            "City": "Washington",
            "StateProvinceCode": "DC",
            "CountryCode": "US",
            "PostalCode": "20057"
        },
        "1126 Queens Hwy Long Beach, CA 90802": {
            "City": "Long Beach",
            "StateProvinceCode": "CA",
            "CountryCode": "US",
            "PostalCode": "90802"
        },
        "2 Rue Marconi 57070 Metz France": {
            "City": "Metz",
            "StateProvinceCode": "",
            "CountryCode": "FR",
            "PostalCode": "57070"
        }
    }

    # Move the address selection to the sidebar
    selected_address = st.sidebar.selectbox(
        "Select an address:",
        list(address_mapping.keys())
    )

    ship_to = address_mapping[selected_address]

    # Move the box size selection to the sidebar
    box_size = st.sidebar.selectbox(
        "Choose a box size:",
        ("6x4x4", "7x5x5", "10x6x4")
    )

    # Move the box weight selection to the sidebar
    box_weight = st.sidebar.selectbox(
        "Choose a box weight:",
        ("1.2", "1.5", "2.0")
    )

    # Display the selected box size
    st.info(f"{box_weight}lb {box_size} box to be shipped to {selected_address}:")

    if st.button("Calculate Price"):
        # Define the ship_from and ship_to addresses
        ship_from = {
            "City": "College Park",
            "StateProvinceCode": "GA",
            "CountryCode": "US",
            "PostalCode": "30337"
        }

        # Define the package details
        package = {
            "PackagingType": {
                "Code": "02"
            },
            "Dimensions": {
                "UnitOfMeasurement": {
                    "Code": "IN"
                },
                "Length": box_size.split('x')[0],
                "Width": box_size.split('x')[1],
                "Height": box_size.split('x')[2]
            },
            "PackageWeight": {
                "UnitOfMeasurement": {
                    "Code": "LBS"
                },
                "Weight": box_weight
            }
        }

        # Call the UPS API to get the shipping rate
        rate_response = get_ups_shipping_rate(access_token, ship_from, ship_to, package)

        # Display the rate
        st.write("Estimated Shipping Rate:", rate_response)

elif option == "Estimated Delivery":
    st.header("Estimated Delivery")
    
    # Define a mapping of addresses to their components
    address_mapping = {
        "1869 Rugby Ave College Park, GA 30337 USA": {
            "City": "College Park",
            "StateProvinceCode": "GA",
            "CountryCode": "US",
            "PostalCode": "30337"
        },
        "211 Longview Ave. Unit 309 Celebration, FL": {
            "City": "Celebration",
            "StateProvinceCode": "FL",
            "CountryCode": "US",
            "PostalCode": "34747"
        },
        "17757 Front Beach Rd. Unit 1809 Panama City Beach, FL 32413": {
            "City": "Panama City Beach",
            "StateProvinceCode": "FL",
            "CountryCode": "US",
            "PostalCode": "32413"
        },
        "37th St NW & O St NW Office 302 Washington, DC 20057": {
            "City": "Washington",
            "StateProvinceCode": "DC",
            "CountryCode": "US",
            "PostalCode": "20057"
        },
        "1126 Queens Hwy Long Beach, CA 90802": {
            "City": "Long Beach",
            "StateProvinceCode": "CA",
            "CountryCode": "US",
            "PostalCode": "90802"
        },
        "2 Rue Marconi 57070 Metz France": {
            "City": "Metz",
            "StateProvinceCode": "",
            "CountryCode": "FR",
            "PostalCode": "57070"
        }
    }
    
    # Move the address selection to the sidebar
    selected_address = st.sidebar.selectbox(
        "Select an address:",
        list(address_mapping.keys())
    )

    ship_to = address_mapping[selected_address]

    # Move the box size selection to the sidebar
    box_size = st.sidebar.selectbox(
        "Choose a box size:",
        ("6x4x4", "7x5x5", "10x6x4")
    )

    # Move the box weight selection to the sidebar
    box_weight = st.sidebar.number_input(
        "Package Weight (LBS):",
        min_value=0.1,
        value=10.5,
        step=0.1
    )

    if st.button("Get Estimated Delivery"):
        delivery_data = {
            "originCountryCode": "US",
            "originStateProvince": "GA",
            "originCityName": "College Park",
            "originPostalCode": "30337",
            "destinationCountryCode": ship_to["CountryCode"],
            "destinationStateProvince": ship_to["StateProvinceCode"],
            "destinationCityName": ship_to["City"],
            "destinationPostalCode": ship_to["PostalCode"],
            "weight": str(box_weight),
            "weightUnitOfMeasure": "LBS",
            "shipmentContentsValue": str(box_weight),
            "shipmentContentsCurrencyCode": "USD",
            "billType": "03",
            "shipDate": datetime.now().strftime("%Y-%m-%d"),
            "shipTime": "",
            "residentialIndicator": "",
            "avvFlag": True,
            "numberOfPackages": "1"
        }
        
        delivery_response = get_ups_estimated_delivery(access_token, delivery_data)
        services = delivery_response["emsResponse"]["services"]

        for service in services:
            service_level_description = service["serviceLevelDescription"]
            delivery_date = service["deliveryDate"]
            st.write(f"{service_level_description} arrives on {delivery_date}")

elif option == "Coming Soon...":
    st.write("Stay tuned for more features!")
elif option == "UPS OAuth":
    st.header("UPS OAuth")
    st.write("This is a test of the UPS OAuth functionality.")
    if st.button("Get Access Token"):
        access_token = get_ups_token(client_id, client_secret)
        st.success(f"Successful OAuth! Access Token: {access_token}")
        st.session_state["access_token"] = access_token
