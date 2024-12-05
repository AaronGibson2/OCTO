# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import osmnx as ox
import os

# Download GraphML files for a list of cities using osmnx and save them locally.
def download_graphml_for_cities(cities, output_folder="graphml_files"):

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for city in cities:
        try:
            print(f"Downloading graph for {city}...")

            # Download the street network graph for the city
            graph = ox.graph_from_place(city, network_type="drive")

            # Format city name to create a valid filename
            filename = city.replace(", ", "_").replace(" ", "_").replace("/", "-") + ".graphml"
            filepath = os.path.join(output_folder, filename)

            # Save the graph to a GraphML file
            ox.save_graphml(graph, filepath)
            print(f"Graph for {city} saved to {filepath}")
        except Exception as e:
            print(f"Failed to download graph for {city}. Error: {e}")

# M A I N ----------------------------------------------------------
if __name__ == "__main__":

    # Major cities in Florida
    cities_in_florida = [
        "Miami, Florida, USA",
        "Orlando, Florida, USA",
        "Tampa, Florida, USA",
        "Jacksonville, Florida, USA",
        "Tallahassee, Florida, USA",
        "Fort Lauderdale, Florida, USA",
        "St. Petersburg, Florida, USA",
        "Cape Coral, Florida, USA",
        "Pembroke Pines, Florida, USA",
        "Gainesville, Florida, USA"
    ]

    # Download GraphML files for these cities
    download_graphml_for_cities(cities_in_florida)
