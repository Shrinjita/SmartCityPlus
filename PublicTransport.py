import streamlit as st
import osmnx as ox
import networkx as nx
import plotly.graph_objects as go
from geopy.geocoders import Nominatim


# -------------------- #
# 🚍 PUBLIC TRANSPORTATION MODULE #
# -------------------- #

def public_transport():
    st.title("🚍 Chennai Route Optimizer")
    st.markdown("Enter your start and destination locations to find the best route.")

    # User Input
    origin = st.text_input("Enter Start Location", "Chennai Central")
    destination = st.text_input("Enter Destination", "Marina Beach")

    # Geocode locations
    def get_coordinates(location):
        geolocator = Nominatim(user_agent="route_optimizer", timeout=10)
        loc = geolocator.geocode(location)
        return (loc.latitude, loc.longitude) if loc else None

    if st.button("Find Optimized Route"):
        origin_point = get_coordinates(origin)
        destination_point = get_coordinates(destination)

        if origin_point and destination_point:
            # Download road network
            with st.spinner("Loading Chennai road network..."):
                G = ox.graph_from_place("Chennai, India", network_type='drive')
                G = nx.DiGraph(G)

            # Find nearest nodes
            origin_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0])
            destination_node = ox.distance.nearest_nodes(G, destination_point[1], destination_point[0])

            # Compute shortest path
            shortest_path = nx.shortest_path(G, origin_node, destination_node, weight='length')

            # Extract route coordinates
            route_nodes = [(G.nodes[node]['x'], G.nodes[node]['y']) for node in shortest_path]
            lons, lats = zip(*route_nodes)

            # Plot Route with Plotly
            fig = go.Figure()
            
            # Add route line
            fig.add_trace(go.Scattermapbox(
                mode="lines+markers",
                lon=lons, lat=lats,
                marker={'size': 10, 'color': 'blue'},
                line=dict(width=4, color='red'),
                name="Optimized Route"
            ))

            fig.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    zoom=12, 
                    center=dict(lat=origin_point[0], lon=origin_point[1])
                ),
                margin={"r": 0, "t": 0, "l": 0, "b": 0}
            )

            # Display the route
            st.plotly_chart(fig)

            # Display route details
            st.success(f"Optimized Route Found ✅")
            st.write(f"**Start:** {origin} → **Destination:** {destination}")
            st.write(f"**Distance:** {nx.shortest_path_length(G, origin_node, destination_node, weight='length') / 1000:.2f} km")
        else:
            st.error("Could not geocode the locations. Please enter valid places.")
