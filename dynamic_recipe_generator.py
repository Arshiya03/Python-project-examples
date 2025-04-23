import random
import datetime
import pytz

class RecipeGenerator:
    def __init__(self):
        self.cuisine_data = {
            "italian": {
                "key_ingredients": ["tomato", "olive oil", "garlic", "basil", "oregano", "pasta", "cheese", "mozzarella"],
                "common_pairings": [("tomato", "basil"), ("garlic", "olive oil"), ("mozzarella", "tomato"), ("parmesan", "pasta")],
                "flavor_profile": ["savory", "herby", "fresh", "rich"],
                "typical_techniques": ["sautéing", "boiling", "baking", "simmering"],
                "meal_starters": {
                    "breakfast": ["eggs", "bread", "coffee"],
                    "lunch": ["pasta", "salad", "sandwich"],
                    "dinner": ["pasta", "pizza", "risotto", "meat", "fish"],
                    "snack": ["cheese", "olives", "bread"]
                },
                "recipe_hints": {
                    "pasta": [
                        {"ingredients": ["tomato", "garlic", "olive oil", "basil"], "description": "a simple tomato sauce pasta"},
                        {"ingredients": ["cream", "parmesan", "butter"], "description": "a creamy Alfredo pasta"},
                        {"ingredients": ["ground meat", "tomato", "onion"], "description": "a classic Bolognese pasta"}
                    ],
                    "pizza": [
                        {"ingredients": ["tomato sauce", "mozzarella", "basil"], "description": "a Margherita pizza"},
                        {"ingredients": ["tomato sauce", "mozzarella", "pepperoni"], "description": "a pepperoni pizza"},
                        {"ingredients": ["barbecue sauce", "mozzarella", "onion", "chicken"], "description": "a BBQ chicken pizza"}
                    ],
                    "salad": [
                        {"ingredients": ["lettuce", "tomato", "cucumber", "olives", "onion"], "description": "a basic Italian salad with vinaigrette"}
                    ]
                }
            },
            "indian": {
                "key_ingredients": ["onion", "ginger", "garlic", "turmeric", "cumin", "coriander", "chili", "mustard oil", "ghee", "rice", "lentils"],
                "common_pairings": [("onion", "tomato"), ("ginger", "garlic"), ("cumin", "coriander"), ("turmeric", "chili")],
                "flavor_profile": ["spicy", "aromatic", "savory", "earthy"],
                "typical_techniques": ["sautéing", "braising", "tempering", "stewing"],
                "meal_starters": {
                    "breakfast": ["eggs", "bread", "yogurt"],
                    "lunch": ["rice", "lentils", "vegetables"],
                    "dinner": ["curry", "rice", "naan"],
                    "snack": ["spiced nuts", "fritters"]
                },
                "recipe_hints": {
                    "curry": [
                        {"ingredients": ["onion", "tomato", "ginger", "garlic", "turmeric", "cumin", "coriander"], "description": "a basic curry base"},
                        {"ingredients": ["chicken", "onion", "tomato", "ginger", "garlic", "spices"], "description": "a chicken curry"},
                        {"ingredients": ["potatoes", "cauliflower", "onion", "tomato", "spices"], "description": "an aloo gobi (potato and cauliflower curry)"}
                    ],
                    "dal": [
                        {"ingredients": ["lentils", "turmeric", "cumin", "onion", "tomato"], "description": "a simple lentil dal"},
                        {"ingredients": ["lentils", "spinach", "ginger", "garlic", "spices"], "description": "a palak dal (spinach lentil curry)"}
                    ]
                }
            },
            "mexican": {
                "key_ingredients": ["corn", "beans", "chili", "tomato", "onion", "garlic", "lime", "cilantro", "avocado", "tortillas"],
                "common_pairings": [("tomato", "onion"), ("chili", "lime"), ("beans", "corn"), ("avocado", "cilantro")],
                "flavor_profile": ["spicy", "tangy", "fresh", "hearty"],
                "typical_techniques": ["grilling", "roasting", "simmering", "frying"],
                "meal_starters": {
                    "breakfast": ["eggs", "tortillas", "beans"],
                    "lunch": ["tacos", "burritos", "salad"],
                    "dinner": ["enchiladas", "fajitas", "chili"],
                    "snack": ["salsa", "guacamole", "chips"]
                },
                "recipe_hints": {
                    "tacos": [
                        {"ingredients": ["tortillas", "ground meat", "onion", "salsa", "lettuce"], "description": "basic ground beef tacos with lettuce"},
                        {"ingredients": ["tortillas", "chicken", "peppers", "onion"], "description": "chicken fajita tacos"}
                    ],
                    "salad": [
                        {"ingredients": ["lettuce", "tomato", "onion", "corn", "beans", "avocado"], "description": "a Mexican bean and corn salad"}
                    ]
                }
            },
            "american": {
                "key_ingredients": ["beef", "chicken", "bread", "cheese", "lettuce", "tomato", "onion", "barbecue sauce"],
                "common_pairings": [("beef", "cheese"), ("chicken", "barbecue sauce"), ("lettuce", "tomato")],
                "flavor_profile": ["savory", "smoky", "rich", "fresh"],
                "typical_techniques": ["grilling", "baking", "frying"],
                "meal_starters": {
                    "breakfast": ["eggs", "bacon", "pancakes"],
                    "lunch": ["sandwich", "burger", "salad"],
                    "dinner": ["steak", "grilled chicken", "pasta"],
                    "snack": ["chips", "pretzels"]
                },
                "recipe_hints": {
                    "burger": [
                        {"ingredients": ["beef", "bread", "cheese", "lettuce", "tomato", "onion", "barbecue sauce"], "description": "a classic BBQ cheeseburger"},
                        {"ingredients": ["chicken", "bread", "lettuce", "tomato", "ranch dressing"], "description": "a chicken ranch sandwich"}
                    ],
                    "salad": [
                        {"ingredients": ["lettuce", "cucumber", "tomato", "onion", "ranch dressing"], "description": "a simple garden salad with ranch"}
                    ]
                }
            }
        }
        self.dressing_options = ["ranch dressing", "creamy tangy garlic aioli", "barbecue sauce"]
        self.fresh_ingredients = ["lettuce", "cucumbers", "onion", "olives", "spring onion"]

    def suggest_meal_type(self):
        current_hour = int(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%H"))
        if 6 <= current_hour < 10:
            return "breakfast"
        elif 12 <= current_hour < 14:
            return "lunch"
        elif 18 <= current_hour < 22:
            return "dinner"
        else:
            return "snack"

    def analyze_ingredients(self, ingredients, cuisine):
        cuisine_info = self.cuisine_data.get(cuisine.lower())
        if not cuisine_info:
            return {"key_ingredients_present": [], "common_pairings_present": []}

        key_ingredients_present = [ing for ing in ingredients if ing.lower() in [ki.lower() for ki in cuisine_info.get("key_ingredients", [])]]
        common_pairings_present = []
        for pair in cuisine_info.get("common_pairings", []):
            if pair[0].lower() in [ing.lower() for ing in ingredients] and pair[1].lower() in [ing.lower() for ing in ingredients]:
                common_pairings_present.append(pair)

        fresh_present = [ing for ing in ingredients if ing.lower() in [fi.lower() for fi in self.fresh_ingredients]]
        dressing_present = [ing for ing in ingredients if ing.lower() in [di.lower() for di in self.dressing_options]]

        return {"key_ingredients_present": key_ingredients_present,
                "common_pairings_present": common_pairings_present,
                "fresh_ingredients_present": fresh_present,
                "dressing_present": dressing_present}

    def generate_recipe(self, ingredients, cuisine, meal_type=None):
        cuisine = cuisine.lower()
        cuisine_info = self.cuisine_data.get(cuisine)
        if not cuisine_info:
            return f"Sorry, I don't have recipe ideas for {cuisine} cuisine yet."

        if not meal_type:
            meal_type = self.suggest_meal_type()

        print(f"\nOkay, let's try to create a {cuisine} {meal_type} idea using: {', '.join(ingredients)}")

        analysis = self.analyze_ingredients(ingredients, cuisine)
        key_ingredients = analysis["key_ingredients_present"]
        pairings = analysis["common_pairings_present"]
        fresh_present = analysis["fresh_ingredients_present"]
        dressing_present = analysis["dressing_present"]

        possible_recipes = []
        if cuisine_info.get("recipe_hints"):
            for recipe_type, hints in cuisine_info["recipe_hints"].items():
                for hint in hints:
                    if all(ing.lower() in [i.lower() for i in ingredients] for ing in hint["ingredients"]):
                        possible_recipes.append(f"Consider making {hint['description']} ({recipe_type} style).")

        if possible_recipes:
            print("\nHere are some specific ideas based on your ingredients:")
            for i, recipe in enumerate(possible_recipes):
                print(f"{i+1}. {recipe}")
        else:
            print("\nHere are some general ideas based on the cuisine and your ingredients:")
            starter_options = list(cuisine_info.get("meal_starters", {}).get(meal_type, []))
            if starter_options:
                starter = random.choice(starter_options)
                suggestion = f"- Perhaps a {starter} with some of your ingredients like {', '.join(key_ingredients[:2]) if key_ingredients else '...'}"
                if fresh_present:
                    suggestion += f", maybe with a fresh topping of {random.choice(fresh_present)}."
                if dressing_present:
                    suggestion += f" You could also consider adding some {random.choice(dressing_present)}."
                print(suggestion)
            else:
                general_suggestion = "- You could try a simple dish focusing on the key flavors of the cuisine using the ingredients you have."
                if fresh_present:
                    general_suggestion += f" Consider adding some fresh elements like {', '.join(fresh_present)}."
                if dressing_present:
                    general_suggestion += f" A drizzle of {random.choice(dressing_present)} might also be interesting."
                print(general_suggestion)

        if pairings:
            print("\nIt looks like you have some classic pairings like:")
            for pair in pairings:
                print(f"- {pair[0]} and {pair[1]}")
                print(f"Consider using them together for a more authentic flavor.")

        if fresh_present:
            print("\nWith your fresh ingredients:")
            print(f"- You could create a simple side salad with {', '.join(fresh_present)}.")

        if dressing_present:
            print("\nRegarding your dressings:")
            print(f"- You could use {', '.join(dressing_present)} as a dip, a salad dressing, or a sauce for your main dish.")

        print("\nTo make this more concrete, could you tell me if you have a main ingredient you'd like to focus on, or any specific dish type in mind?")
        return None

    def get_detailed_recipe(self, ingredients, cuisine, dish_type):
        cuisine = cuisine.lower()
        cuisine_info = self.cuisine_data.get(cuisine)
        if not cuisine_info or not cuisine_info.get("recipe_hints") or dish_type.lower() not in cuisine_info["recipe_hints"]:
            return f"Sorry, I don't have detailed recipe for '{dish_type}' in {cuisine} cuisine right now."

        hints = cuisine_info["recipe_hints"][dish_type.lower()]
        possible_hint = next((hint for hint in hints if all(ing.lower() in [i.lower() for i in ingredients] for ing in hint["ingredients"])), None)

        if possible_hint:
            print(f"\nDetailed recipe idea for {possible_hint['description']}:")
            print("(This is a basic outline, feel free to adjust quantities and add your own touch!)")
            main_ingredients = ", ".join(possible_hint['ingredients'])
            print(f"\nMain Ingredients: {main_ingredients}")

            if dish_type.lower() == "pasta" and "tomato" in possible_hint['ingredients'] and "garlic" in possible_hint['ingredients']:
                print("\nInstructions for Simple Tomato Sauce Pasta:")
                print("1. Heat olive oil in a pan and sauté minced garlic until fragrant.")
                print("2. Add crushed tomatoes and simmer for 15-20 minutes. Season with salt, pepper, and oregano.")
                if "basil" in possible_hint['ingredients']:
                    print("3. Stir in fresh basil at the end.")
                print("4. Cook your favorite pasta according to package directions until al dente.")
                print("5. Toss the pasta with the tomato sauce. Top with grated parmesan cheese if desired.")
            elif dish_type.lower() == "pizza":
                print("\nInstructions for Pizza:")
                print("1. Preheat your oven to a high temperature (e.g., 220°C/428°F).")
                if "tomato sauce" in possible_hint['ingredients']:
                    print("2. Spread tomato sauce (or barbecue sauce if making BBQ chicken pizza) evenly over a pizza base.")
                if "mozzarella" in possible_hint['ingredients']:
                    print("3. Sprinkle with mozzarella cheese.")
                if "basil" in possible_hint['ingredients']:
                    print("4. Add fresh basil leaves.")
                if "pepperoni" in possible_hint['ingredients']:
                    print("5. Arrange pepperoni slices on top.")
                if "onion" in possible_hint['ingredients'] and "barbecue sauce" in possible_hint['ingredients'] and "chicken" in possible_hint['ingredients']:
                    print("6. Add thinly sliced red onion and cooked chicken pieces.")
                print("7. Bake for 10-15 minutes or until the crust is golden and the cheese is melted and bubbly.")
                if "lettuce" in possible_hint['ingredients']:
                    print("8. After baking, top with shredded lettuce.")
            elif dish_type.lower() == "salad":
                print("\nInstructions for Salad:")
                print("1. Wash and chop the lettuce and cucumbers.")
                print("2. Slice the tomatoes and onion.")
                print("3. Combine all the vegetables in a bowl.")
                print("4. Add olives and spring onion.")
                if "ranch dressing" in ingredients:
                    print("5. Drizzle with ranch dressing.")
                elif "creamy tangy garlic aioli" in ingredients:
                    print("5. Drizzle with creamy tangy garlic aioli.")
                elif "barbecue sauce" in ingredients:
                    print("5. You can even try a drizzle of barbecue sauce for a unique flavor!")
                print("6. Toss gently and serve.")
            # Add more detailed instructions for other dish types as needed
            else:
                print("\nDetailed instructions for this specific combination are not available right now, but you can find many recipes online for this basic idea!")
        else:
            print(f"No specific recipe found for '{dish_type}' using all of your provided ingredients in {cuisine} cuisine. However, you can still try a basic version with the key ingredients and perhaps a dressing like {random.choice(self.dressing_options) if self.dressing_options else 'one of your dressings'}.")
        return None

if __name__ == "__main__":
    recipe_gen = RecipeGenerator()

    print("Welcome back to the AI Recipe Generator!")

    while True:
        print("\nWhat would you like to do?")
        print("1. Get recipe ideas based on ingredients and cuisine.")
        print("2. Get a more detailed recipe for a specific dish.")
        print("3. Exit.")

        choice = input("Enter your choice: ")

        if choice == '1':
            ingredients_input = input("Enter your ingredients (comma-separated): ").split(',')
            ingredients = [ing.strip() for ing in ingredients_input]
            cuisine_input = input("Enter the cuisine you're interested in (e.g., Italian, Indian, American): ")
            recipe_gen.generate_recipe(ingredients, cuisine_input)
        elif choice == '2':
            ingredients_input = input("Enter the ingredients you plan to use (comma-separated): ").split
