import random
''' 
Chooses a random weather effect from different weather conditions.
Takes distance to a next airport.
Returns new distance after the weather effects.   
'''

def randomize_weather(gap):
    weather_list= ["clear_sky", "foggy", "rainy", "stormy"]
    result = random.choice(weather_list)
    if result == "clear_sky":
        new_gap = gap
        print("The weather is clear.")
    elif result == "foggy":
        new_gap = (gap * 1.25)
        print(f"The weather is foggy, you used 25% more battery.")
    elif result == "rainy":
        new_gap = (gap * 1.50)
        print(f"The weather is rainy, you used 50% more battery.")
    elif result == "stormy":
        new_gap = (gap * 2)
        print(f"The weather is stormy, you used 100% more battery.")
    return new_gap


#call function here
distance = next_airport[1]
battery -= randomize_weather(distance)