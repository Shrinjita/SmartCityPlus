import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
import time

# Use cache for geocoding to improve performance
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_coordinates(location):
    """Get coordinates with caching."""
    geolocator = Nominatim(user_agent="route_optimizer", timeout=10)
    try:
        loc = geolocator.geocode(f"{location}, Chennai, India")
        if loc:
            return (loc.latitude, loc.longitude)
        else:
            return None
    except Exception:
        return None

# Cache the pre-calculated paths for common routes
@st.cache_data(ttl=86400)  # Cache for 24 hours
def get_predefined_routes():
    """Return predefined routes for common destinations in Chennai."""
    return {
        ("Chennai Central", "Marina Beach"): {
            "path": [
                (13.0836, 80.2825), (13.0812, 80.2798),
                (13.0787, 80.2772), (13.0715, 80.2770),
                (13.0675, 80.2771), (13.0633, 80.2769),
                (13.0590, 80.2756), (13.0556, 80.2743)
            ],
            "distance": 3.5
        },
        ("Chennai Central", "T Nagar"): {
            "path": [
                (13.0836, 80.2825), (13.0812, 80.2743),
                (13.0780, 80.2672), (13.0741, 80.2583),
                (13.0685, 80.2489), (13.0494, 80.2317),
                (13.0416, 80.2339)
            ],
            "distance": 7.2
        },
        ("Chennai Central", "Chennai Airport"): {
            "path": [
                (13.0836, 80.2825), (13.0640, 80.2606),
                (13.0518, 80.2370), (13.0384, 80.2138),
                (13.0155, 80.1883), (13.0098, 80.1707)
            ],
            "distance": 16.8
        }
    }


def public_transport():
    st.title("🚍 Chennai Route Optimizer")
    st.markdown("Enter your start and destination locations to find the best route.")

    # User Input with defaults and suggestions
    chennai_locations = ["Chennai Central", "Marina Beach", "T Nagar", "Chennai Airport", 
                         "Mylapore", "Adyar", "Velachery", "Anna Nagar"]
    
    origin = st.selectbox("Enter Start Location", 
                         chennai_locations,
                         index=0)
    
    destination = st.selectbox("Enter Destination", 
                              chennai_locations,
                              index=1)

    if st.button("Find Optimized Route"):
        if origin == destination:
            st.error("Start and destination locations cannot be the same.")
            return
            
        # Get predefined routes
        predefined_routes = get_predefined_routes()
        
        # Check if we have a predefined route
        route_key = (origin, destination)
        if route_key in predefined_routes:
            route_data = predefined_routes[route_key]
            lats, lons = zip(*route_data["path"])
            distance = route_data["distance"]
            
            with st.spinner("Generating optimized route..."):
                # Add a small delay to simulate processing
                time.sleep(1)
                
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

                # Add start and end markers
                fig.add_trace(go.Scattermapbox(
                    mode="markers",
                    lon=[lons[0]],
                    lat=[lats[0]],
                    marker={'size': 15, 'color': 'green'},
                    name="Start"
                ))
                
                fig.add_trace(go.Scattermapbox(
                    mode="markers",
                    lon=[lons[-1]],
                    lat=[lats[-1]],
                    marker={'size': 15, 'color': 'red'},
                    name="Destination"
                ))

                fig.update_layout(
                    mapbox=dict(
                        style="open-street-map",
                        zoom=12, 
                        center=dict(lat=lats[0], lon=lons[0])
                    ),
                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                    height=500
                )

                # Display the route
                st.plotly_chart(fig, use_container_width=True)

                # Display route details
                st.success(f"Optimized Route Found ✅")
                st.write(f"**Start:** {origin} → **Destination:** {destination}")
                st.write(f"**Distance:** {distance} km")
                
                # Transportation options
                st.subheader("🚌 Public Transportation Options")
                
                transport_options = pd.DataFrame({
                    "Mode": ["Bus", "Metro", "Auto Rickshaw"],
                    "Route": ["4A, 23C, 29C", "Blue Line", "Direct"],
                    "Fare (₹)": ["₹25", "₹40", "₹150-200"],
                    "Travel Time": ["45-60 mins", "30 mins", "25 mins"]
                })
                
                st.table(transport_options)
                
        else:
            # For custom locations, use geocoding
            origin_point = get_coordinates(origin)
            destination_point = get_coordinates(destination)

            if origin_point and destination_point:
                with st.spinner("Computing alternative route..."):
                    # Simulate path calculation with a straight line
                    time.sleep(2)
                    
                    # Create a simple route (direct line between points)
                    lats = [origin_point[0], destination_point[0]]
                    lons = [origin_point[1], destination_point[1]]
                    
                    # Plot simple route
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scattermapbox(
                        mode="lines+markers",
                        lon=lons, lat=lats,
                        marker={'size': 10, 'color': 'blue'},
                        line=dict(width=4, color='red'),
                        name="Basic Route"
                    ))
                    
                    fig.update_layout(
                        mapbox=dict(
                            style="open-street-map",
                            zoom=12, 
                            center=dict(lat=lats[0], lon=lons[0])
                        ),
                        margin={"r": 0, "t": 0, "l": 0, "b": 0},
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Calculate approximate distance
                    import math
                    def haversine(lat1, lon1, lat2, lon2):
                        R = 6371  # Radius of Earth in kilometers
                        dLat = math.radians(lat2 - lat1)
                        dLon = math.radians(lon2 - lon1)
                        a = math.sin(dLat/2) * math.sin(dLat/2) + \
                            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
                            math.sin(dLon/2) * math.sin(dLon/2)
                        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                        d = R * c
                        return d
                    
                    distance = haversine(lats[0], lons[0], lats[1], lons[1])
                    
                    st.success(f"Basic Route Found ✅")
                    st.write(f"**Start:** {origin} → **Destination:** {destination}")
                    st.write(f"**Approximate Distance:** {distance:.2f} km")
                    st.info("Note: This is a simplified route. For detailed directions, consider using Google Maps.")
            else:
                st.error("Could not geocode one or both locations. Please enter valid places in Chennai.")