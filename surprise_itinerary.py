import random
from datetime import datetime, timedelta
import pytz

class TravelPlanner:
    def __init__(self):
        self.destinations_data = {
            "bahrain": {
                "activities": [
                    {"name": "Explore Manama Souq spice stalls", "rating": 4.2, "cost": 0},
                    {"name": "Browse Manama Souq handicrafts", "rating": 4.0, "cost": 0},
                    {"name": "Try Machboos at a local restaurant", "rating": 4.5, "cost": 10},
                    {"name": "Visit Bahrain National Museum", "rating": 4.4, "cost": 2},
                    {"name": "Tour Al-Fateh Grand Mosque", "rating": 4.6, "cost": 0},
                    {"name": "Wander Block 338 art galleries", "rating": 4.1, "cost": 0},
                    {"name": "Relax at [Beach Name]", "rating": 4.3, "cost": 0},
                    {"name": "Spa at [Resort Name]", "rating": 4.7, "cost": 50},
                    {"name": "Hawar Islands day trip", "rating": 4.0, "cost": 30},
                    {"name": "Lost Paradise of Dilmun Water Park", "rating": 4.4, "cost": 40},
                    {"name": "Sunset viewing", "rating": 4.5, "cost": 0}
                ],
                "accommodations": [
                    {"name": "Budget Inn Manama", "rating": 3.5, "price_per_night": 45},
                    {"name": "Mid-Range Hotel Bahrain City", "rating": 4.1, "price_per_night": 80},
                    {"name": "Luxury Resort [Resort Name]", "rating": 4.8, "price_per_night": 150}
                ],
                "food": [
                    {"name": "Machboos", "avg_cost": 10},
                    {"name": "Balaleet", "avg_cost": 8},
                    {"name": "Shawarma", "avg_cost": 5},
                    {"name": "Luqaimat", "avg_cost": 3}
                ]
            }
        }
        self.user_itineraries = {}

    def get_destination_details(self, destination):
        return self.destinations_data.get(destination.lower())

    def generate_single_itinerary(self, destination, budget=None, num_days=3, itinerary_id=None):
        """Generates a single random, budget-friendly itinerary with an ID."""
        details = self.get_destination_details(destination)
        if not details:
            return "Destination not found."

        itinerary = {"id": itinerary_id if itinerary_id is not None else f"itinerary_{random.randint(100, 999)}",
                     "destination": destination, "days": []}
        possible_activities = details.get("activities", [])
        possible_accommodations = details.get("accommodations", [])
        possible_food = details.get("food", [])

        if not possible_activities or not possible_accommodations or not possible_food:
            return "Insufficient data for a surprise itinerary for this destination."

        daily_budget = budget / num_days if budget else None

        for day in range(num_days):
            daily_plan = {"day": day + 1, "activities": [], "accommodation": None, "food": []}

            affordable_activities = [act for act in possible_activities if not daily_budget or act.get("cost", 0) <= daily_budget / 3]
            daily_plan["activities"].append(random.choice(affordable_activities) if affordable_activities else random.choice(possible_activities))

            affordable_accommodations = [acc for acc in possible_accommodations if not daily_budget or acc.get("price_per_night", 0) <= daily_budget / 2]
            daily_plan["accommodation"] = random.choice(affordable_accommodations) if affordable_accommodations else random.choice(possible_accommodations)

            affordable_food = [food for food in possible_food if not daily_budget or food.get("avg_cost", 0) <= daily_budget / 4]
            daily_plan["food"].append(random.choice(affordable_food) if affordable_food else random.choice(possible_food))
            if random.random() < 0.7:
                daily_plan["food"].append(random.choice(possible_food))

            itinerary["days"].append(daily_plan)

        return itinerary

    def generate_multiple_itineraries(self, destination, num_itineraries=3, budget=None, num_days=3):
        """Generates a dictionary of multiple random itineraries."""
        itineraries = {}
        for i in range(num_itineraries):
            itinerary_id = f"itinerary_{i+1}"
            itineraries[itinerary_id] = self.generate_single_itinerary(destination, budget, num_days, itinerary_id)
        return itineraries

    def display_itinerary(self, itinerary):
        if isinstance(itinerary, str):
            print(itinerary)
            return

        print(f"\n--- Itinerary: {itinerary.get('id', 'No ID')} for {itinerary['destination']} ---")
        for day_plan in itinerary["days"]:
            print(f"\n**Day {day_plan['day']}**")
            print(f"  Accommodation: {day_plan['accommodation']['name']} (Rated: {day_plan['accommodation']['rating']})")
            print("  Activities:")
            for activity in day_plan["activities"]:
                print(f"    - {activity['name']} (Rated: {activity.get('rating', 'N/A')}, Est. Cost: ${activity.get('cost', 0)})")
            print("  Food:")
            for food in day_plan["food"]:
                print(f"    - {food['name']} (Est. Avg. Cost: ${food.get('avg_cost', 0)})")
        print("-----------------------------------------\n")

    def display_multiple_itineraries(self, itineraries):
        """Displays all the generated itineraries in the dictionary."""
        print("\n--- Multiple Surprise Itineraries ---")
        for itinerary_id, itinerary_data in itineraries.items():
            self.display_itinerary(itinerary_data)
        print("-------------------------------------\n")

    def get_booking_options(self, itinerary):
        booking_options = []
        for day_plan in itinerary["days"]:
            accommodation = day_plan["accommodation"]
            booking_options.append({
                "type": "accommodation",
                "name": accommodation["name"],
                "rating": accommodation["rating"],
                "price_per_night": accommodation["price_per_night"],
                "availability": random.randint(5, 20) > 0,
                "itinerary_id": itinerary.get("id")
            })
            for activity in day_plan["activities"]:
                booking_options.append({
                    "type": "activity",
                    "name": activity["name"],
                    "rating": activity.get("rating", "N/A"),
                    "cost": activity.get("cost", 0),
                    "availability": random.randint(10, 30) > 0,
                    "itinerary_id": itinerary.get("id")
                })
        return booking_options

    def display_booking_options(self, options):
        print("\n--- Booking Options ---")
        rated_options = sorted(options, key=lambda x: x.get('rating', 0) if isinstance(x.get('rating'), (int, float)) else 0, reverse=True)
        for i, option in enumerate(rated_options):
            availability_status = "Available" if option["availability"] else "Not Available"
            price = option.get('price_per_night', option.get('cost', 'N/A'))
            print(f"{i+1}. Itinerary ID: {option.get('itinerary_id', 'N/A')}, Type: {option['type'].capitalize()}, Name: {option['name']}, Rating: {option.get('rating', 'N/A')}, Price: ${price:.2f} (per night/est.), Status: {availability_status}")
        print("-----------------------\n")
        return rated_options

    def get_user_confirmation(self, options):
        while True:
            choices = input("Enter the numbers of the items you want to book (comma-separated), or 'done': ").lower()
            if choices == 'done':
                break
            try:
                selected_indices = [int(x.strip()) - 1 for x in choices.split(',')]
                confirmed_bookings = [options[i] for i in selected_indices if 0 <= i < len(options) and options[i]['availability']]
                if confirmed_bookings:
                    print("\nConfirmed Bookings:")
                    for booking in confirmed_bookings:
                        print(f"- Itinerary ID: {booking.get('itinerary_id', 'N/A')}, {booking['type'].capitalize()}: {booking['name']}")
                    return confirmed_bookings
                else:
                    print("No valid or available items selected. Please try again.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas or 'done'.")
        return []

    def run(self):
        print("Welcome to the Multiple Surprise Itinerary & Booking System!")
        destination = input("Enter your destination: ")
        details = self.get_destination_details(destination)
        if not details:
            print("Destination not found. Exiting.")
            return

        if input("Would you like to generate multiple 'Surprise Me!' itineraries? (yes/no): ").lower() == 'yes':
            num_itineraries = int(input("How many surprise itineraries would you like? ") or 3)
            budget = float(input("Enter your budget for the trip (optional): ") or 0)
            num_days = int(input("How many days will you be traveling? ") or 3)
            multiple_itineraries = self.generate_multiple_itineraries(destination, num_itineraries, budget, num_days)
            self.display_multiple_itineraries(multiple_itineraries)

            if input("Would you like to see booking options for these itineraries? (yes/no): ").lower() == 'yes':
                all_booking_options = []
                for itinerary_id, itinerary_data in multiple_itineraries.items():
                    booking_options = self.get_booking_options(itinerary_data)
                    all_booking_options.extend(booking_options)

                if all_booking_options:
                    rated_options = self.display_booking_options(all_booking_options)
                    self.get_user_confirmation(rated_options)
                else:
                    print("No booking options available for these itineraries.")

        else:
            print("Okay, generating a single surprise itinerary:")
            budget = float(input("Enter your budget for the trip (optional): ") or 0)
            num_days = int(input("How many days will you be traveling? ") or 3)
            single_itinerary = self.generate_single_itinerary(destination, budget, num_days)
            self.display_itinerary(single_itinerary)

            if input("Would you like to see booking options for this itinerary? (yes/no): ").lower() == 'yes':
                booking_options = self.get_booking_options(single_itinerary)
                if booking_options:
                    rated_options = self.display_booking_options(booking_options)
                    self.get_user_confirmation(rated_options)
                else:
                    print("No booking options available for this itinerary.")

if __name__ == "__main__":
    planner = TravelPlanner()
    planner.run()
