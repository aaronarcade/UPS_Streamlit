import streamlit as st

# Set up the sidebar
st.sidebar.title("Options")

# Create a dropdown menu in the sidebar
option = st.sidebar.selectbox(
    "Choose an option:",
    ("Estimated Price", "Estimated Delivery", "Coming Soon...")
)

# Display the selected option
st.write(f"You selected: {option}")

# Add logic for each option
if option == "Estimated Price":
    st.write("Functionality for Estimated Price will be here.")
elif option == "Estimated Delivery":
    st.write("Functionality for Estimated Delivery will be here.")
elif option == "Coming Soon...":
    st.write("Stay tuned for more features!") 