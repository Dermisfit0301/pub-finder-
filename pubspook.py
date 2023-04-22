import streamlit as st



import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objs as go
from scipy.spatial.distance import cdist

# Load the dataset
df = pd.read_csv("open_pubs.csv")

# Define the Streamlit app
def intro():
    st.markdown("<h1 style='color: Purple; font-size: 36px;'>Pubspook</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: Dark Gold; font-size: 36px;'>The barmy ghost who gets you drunk!</h1>", unsafe_allow_html=True)
    st.write("When I was alive I was famous.. No not as a knight or a prince! but as the man who could find the best taverns in town.My talent was known throughout the old World.I died and went to heaven but God sent me back.Why do you ask? To find the best places for you to get booze from! Not to haunt you. Welcome to my app and I will help you find the best places to drink by the options you choose.I can get you the list of the places in that area. So stop scrolling and start boozing!!")
    image = Image.open('pubspooklogo.jpg')
    st.image(image, '')

    if st.button("what if you kill us"):
        st.write("I dont drink blood only booze and I will help you find the best in UK!")



def dashboard():
    st.markdown("<h1 style='color: red; font-size: 36px;'>Some stats to get drunk on!</h1>", unsafe_allow_html=True)

    st.write("Have a quick glance  where the most pubs are:")
    top_regions = df["Region"].value_counts().head(5)
    st.write("## Top 5 Regions by Pub Count")
    st.bar_chart(top_regions)
    num_pubs = df.groupby('Region')['name'].nunique().reset_index(name='Num Pubs')
    compact = pd.merge(df, num_pubs, on='Region')
    fig = px.scatter_mapbox(compact, lat="latitude", lon="longitude", hover_name="name",
                            hover_data={"Region": True, "Num Pubs": True},
                            size="Num Pubs", size_max=20, zoom=5,
                            mapbox_style="carto-positron")
    
    fig.update_layout(
    title="The number of pubs to choose from in UK!!!",
    mapbox=dict(
        
        center=dict(lat=54, lon=-2),
        zoom=5
    ),
    margin=dict(l=0, r=0, t=30, b=0)
)

    st.plotly_chart(fig, use_container_width=True)

def findbylocauth():
    st.title("Find by Local authority")
    st.write("You can select the Local Authority here to find pubs near you.")
    local_authorities = df["local_authority"].unique()
    selected_local_authority = st.selectbox("Select a local authority", local_authorities)
    columns_to_display = ["fsa_id", "name", "address",'Areaname'] 
    filtered_df = df[df["local_authority"] == selected_local_authority]
    st.table(filtered_df[columns_to_display])

def byareaname():
    st.title("Find by Area name")
    st.write("You can select the Area name here to find pubs near you.")
    postal_code = df["Areaname"].unique()
    selected_Areaname= st.selectbox("Select an Area ", postal_code)
    columns_to_display = ["fsa_id", "name", "address",'local_authority' ,'postcode']
    filtered_df = df[df["Areaname"] == selected_Areaname]
    st.table(filtered_df[columns_to_display])

def bycoord():
    def euclidean_distance(lat1, lon1, lat2, lon2):
        return cdist([(lat1, lon1)], [(lat2, lon2)], metric='euclidean')[0][0]
    def find_nearest_pubs(latitude, longitude):
   
        distances = df.apply(lambda row: euclidean_distance(latitude, longitude, row['latitude'], row['longitude']), axis=1)
    
        df['distance'] = distances
    
        nearest_pubs = df.sort_values('distance').head(5)
   
        return nearest_pubs


    st.title('Find the nearest pubs')
    # Get the user's location
    latitude = st.text_input('Enter your latitude')
    longitude = st.text_input('Enter your longitude')
    # Check if the user has entered their location
    if latitude and longitude:
        # Convert the latitude and longitude to floats
        latitude = float(latitude)
        longitude = float(longitude)
        # Find the 5 nearest pubs to the given location
        nearest_pubs = find_nearest_pubs(latitude, longitude)
        # Display the nearest pubs in a table
        st.write(nearest_pubs)
    



# Define the Streamlit app
def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to",["Intro", "Dashboard", "By local authority", "By Area name", "Find by Co-ordinates"])

    # Show the appropriate page based on the user's selection
    if selection == "Intro":
        intro()
    elif selection == "Dashboard":
        dashboard()
    elif selection == "By local authority":
        findbylocauth()
    elif selection == "By Area name":
        byareaname()
    elif selection == "Find by Co-ordinates":
        bycoord()


    














# Run the app
if __name__ == "__main__":
    main()