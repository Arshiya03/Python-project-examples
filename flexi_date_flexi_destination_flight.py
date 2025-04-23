import datetime
from dateutil.relativedelta import relativedelta  # For flexible date calculations
# import requests  # For making HTTP requests to flight data sources (APIs or scraping)
# from bs4 import BeautifulSoup  # For parsing HTML if scraping
import pandas as pd  # For handling and organizing flight data
# import folium  # For map visualization (optional, but cool!)

class FlightExplorer:
    def __init__(self):
        self.flight_data = pd.DataFrame() # Placeholder for flight data

    def get_flexible_dates(self, date_input):
        """
        Interprets user's flexible date input and returns a date range.
        (This would need more sophisticated logic for truly natural language input)
        """
        today = datetime.date.today()
        if "next month" in date_input.lower():
            start_date = today + relativedelta(months=1, day=1)
            end_date = today + relativedelta(months=2, day=1, days=-1)
        elif "long weekend" in date_input.lower():
            # Simple example: next available long weekend (Fri-Sun)
            now = datetime.datetime.now()
            days_until_friday = (4 - now.weekday() + 7) % 7
            start_date = now.date() + datetime.timedelta(days=days_until_friday)
            end_date = start_date + datetime.timedelta(days=2)
        elif "within the next" in date_input.lower():
            try:
                weeks = int(date_input.lower().split("next ")[1].split(" week")[0])
                start_date = today
                end_date = today + datetime.timedelta(weeks=weeks)
            except ValueError:
                return None, None
        else:
            # For simplicity, assume a specific date range if no keywords are found
            return None, None # Need to handle specific date input later

        return start_date, end_date

    def get_region_coordinates(self, region_input):
        """
        Returns approximate latitude and longitude boundaries for a given region.
        (This would need a more comprehensive database or API for regions)
        """
        region_input_lower = region_input.lower()
        if "southern europe" in region_input_lower:
            return (35, -10, 45, 30) # (min_lat, min_lon, max_lat, max_lon)
        elif "southeast asia" in region_input_lower:
            return (-10, 95, 25, 145)
        elif "caribbean" in region_input_lower:
            return (10, -85, 28, -59)
        elif "west coast usa" in region_input_lower:
            return (30, -125, 50, -115)
        else:
            return None # Region not found

    def fetch_flight_data(self, start_date, end_date, region_coords, budget):
        """
        This is the core function to fetch flight data based on criteria.
        (This would involve interacting with flight APIs or scraping websites)
        For now, let's simulate some data.
        """
        if start_date is None or end_date is None or region_coords is None:
            print("Invalid date range or region.")
            return pd.DataFrame()

        min_lat, min_lon, max_lat, max_lon = region_coords
        num_flights = random.randint(5, 20)
        data = []
        for _ in range(num_flights):
            departure_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
            arrival_date = departure_date + datetime.timedelta(hours=random.randint(2, 15))
            price = random.uniform(50, budget)
            latitude = random.uniform(min_lat, max_lat)
            longitude = random.uniform(min_lon, max_lon)
            city = f"City {random.randint(1, 10)}" # Placeholder
            airline = random.choice(["BudgetAir", "FlyLow", "CheapWings"])
            data.append({"departure_date": departure_date, "arrival_date": arrival_date,
                         "price": price, "latitude": latitude, "longitude": longitude,
                         "destination_city": city, "airline": airline})
        self.flight_data = pd.DataFrame(data)
        return self.flight_data

    def filter_flights(self, max_budget=None, max_duration_hours=None, max_stops=None, preferred_airlines=None):
        """
        Filters the fetched flight data based on user preferences.
        """
        filtered_data = self.flight_data.copy()
        if max_budget is not None:
            filtered_data = filtered_data[filtered_data['price'] <= max_budget]
        # Add more filtering logic for duration, stops, airlines later
        return filtered_data

    def sort_flights(self, sort_by="price"):
        """
        Sorts the filtered flight data.
        """
        return self.flight_data.sort_values(by=sort_by)

    def visualize_cheap_destinations(self, filtered_flights):
        """
        (Optional) Uses folium to display cheap destinations on a map.
        """
        if not filtered_flights.empty:
            import folium
            m = folium.Map(location=[filtered_flights['latitude'].mean(), filtered_flights['longitude'].mean()], zoom_start=3)
            for index, row in filtered_flights.iterrows():
                folium.Marker([row['latitude'], row['longitude']],
                              popup=f"{row['destination_city']} - ${row['price']:.2f} ({row['airline']})").add_to(m)
            m.save("cheap_destinations_map.html")
            print("Map of cheap destinations saved to cheap_destinations_map.html")
        else:
            print("No flights found within your criteria to visualize.")

    def run(self):
        print("Welcome to the Flexi-Date, Flexi-Destination Flight Explorer!")

        date_input = input("Enter a flexible date range (e.g., next month, long weekend in the fall, within the next 4 weeks): ")
        start_date, end_date = self.get_flexible_dates(date_input)
        if start_date and end_date:
            print(f"Searching for flights between {start_date} and {end_date}...")
            region_input = input("Enter a broad region you'd like to explore (e.g., Southern Europe, Southeast Asia, Caribbean, West Coast USA): ")
            region_coords = self.get_region_coordinates(region_input)
            if region_coords:
                try:
                    budget = float(input("Enter your maximum budget for the flight: "))
                    print("Fetching flight data...")
                    flights = self.fetch_flight_data(start_date, end_date, region_coords, budget)
                    if not flights.empty:
                        print("\nPotential cheap flights within your criteria:")
                        sorted_flights = self.sort_flights()
                        print(sorted_flights[['departure_date', 'arrival_date', 'destination_city', 'price', 'airline']])

                        visualize = input("\nWould you like to visualize these destinations on a map? (yes/no): ").lower()
                        if visualize == "yes":
                            self.visualize_cheap_destinations(sorted_flights)
                    else:
                        print("No cheap flights found matching your criteria.")
                except ValueError:
                    print("Invalid budget entered.")
            else:
                print("Region not recognized.")
        else:
            print("Invalid date range input.")

if __name__ == "__main__":
    explorer = FlightExplorer()
    explorer.run()
