import mysql.connector
import random
from geopy.distance import geodesic

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='Mooimoipuipoi8181',
         autocommit=True
         )


screen_name = input("Hi there, what is your name?")
airplane_name = input("Hi " + screen_name + ", now you can choose name for your airplane, what would you like to call it?")

story = ("Welcome " + screen_name + ", to the flight adventure!"
         "In this game, you start your journey with your plane " + airplane_name + " from a randomly selected European airport and choose your next destination from three nearby airports."
         "You have a full battery at the beginning, which allows you to fly 2000km"
         "As you travel, you collect points, but remember that your battery consumes energy. "
         "The game ends when the battery is empty. Good luck on your journey and collect as many points as possible!")

print(story)

def random_airport():
    sql = (""" SELECT airport.iso_country, airport.ident, airport.name, airport.type, airport.latitude_deg, airport.longitude_deg, country.name
FROM airport
JOIN country ON airport.iso_country = country.iso_country
WHERE airport.continent = 'EU' 
AND airport.TYPE IN ('large_airport', 'medium_airport' , 'small_airport');""")
    kursori = yhteys.cursor()
    kursori.execute(sql)
    airports = kursori.fetchall()

    return airports



#visited airport's idents will be collected to this list.
visited_airports = []


def nearest_airport(airport, airports, type):
    your_location = (airport[4], airport[5])
    # Poista nykyinen lentokenttä lentokenttälistasta ja lentokentät, jotka ovat samassa maassa
    airports = [a for a in airports if a[0] != airport[0] and a[1] not in visited_airports]
    distances = [(a, geodesic(your_location, (a[4], a[5])).kilometers) for a in airports if a[3] == type]
    nearest_airport = min(distances, key=lambda x: x[1])
    return nearest_airport

#Chooses a random weather effect from different weather conditions.
#Takes distance to a next airport.
#Returns new distance after the weather effects.


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

airports = random_airport()
random_airport_result = random.choice(airports)
# After the first random airport is chosen, append to the visited list.
visited_airports.append(random_airport_result[1])

print("You will start your game at the following airport: ")
print(random_airport_result[2], ",", random_airport_result[6])


nearest_small_airport = nearest_airport(random_airport_result, airports, 'small_airport')
nearest_medium_airport = nearest_airport(random_airport_result, airports, 'medium_airport')
nearest_large_airport = nearest_airport(random_airport_result, airports, 'large_airport')



# Näytä pelaajalle kolme vaihtoehtoa ja pyydä pelaajaa valitsemaan yksi niistä
print("Now you have to choose your next location where you want to go")
print("Here are your options:")
print("1. Small airport, from this airport you will get 1 point: ", nearest_small_airport[0][2], ",", nearest_small_airport[0][6], ",", "Distance:", nearest_small_airport[1], "km")
print("2. Medium airport, from this airport you will get 3 points: ", nearest_medium_airport[0][2], ",", nearest_medium_airport[0][6], ",",  "Distance:", nearest_medium_airport[1], "km")
print("3. Large airport, from this airport you will get 5 points: ", nearest_large_airport[0][2], ",", nearest_large_airport[0][6], ",","Distance:", nearest_large_airport[1], "km")


battery = 2000
points = 0

choice = ''
while choice not in ['1', '2', '3']:
    choice = input("Please choose an option (1, 2, or 3): ")
    if choice == '1':
        next_airport = nearest_small_airport
        points += 1  # Lisää yksi piste pienestä lentokentästä
    elif choice == '2':
        next_airport = nearest_medium_airport
        points += 3  # Lisää kolme pistettä keskikokoisesta lentokentästä
    elif choice == '3':
        next_airport = nearest_large_airport
        points += 5  # Lisää viisi pistettä isosta lentokentästä
    else:
        print("Invalid choice. Please choose 1, 2, or 3.")

visited_airports.append(next_airport[0][1])



print("You have chosen to fly to the following airport: ")
print(next_airport[0][2], ",", next_airport[0][6], "," , next_airport[1],"km")

# Laske matkan pituus ja vähennä se akun tilasta
distance = next_airport[1]  # Oletan, että tämä on matkan pituus
battery -= randomize_weather(distance)

if battery <= 0:
    if next_airport[0][3] == "small_airport":
        points -= 1
    elif next_airport[0][3] == "medium_airport":
        points -= 3
    elif next_airport[0][3] == "large_airport":
        points -= 5

    print("Your airplane's battery is empty. The game has ended.")
    print("Your total points are: " + str(points))
    print("Thank you for playing the game!")
    print("Press any key to quit.")
    input()
    exit()

# Tulosta jäljellä oleva akun tila ja lentomatka
print("Your airplane's battery has now " + str(battery) + "km left.")

# Tulosta pelaajan nykyinen pistemäärä
print("You have now " + str(points) + " points.")

while battery > 0:
    random_airport_result = next_airport[0]
    nearest_small_airport = nearest_airport(random_airport_result, airports, 'small_airport')
    nearest_medium_airport = nearest_airport(random_airport_result, airports, 'medium_airport')
    nearest_large_airport = nearest_airport(random_airport_result, airports, 'large_airport')

    # Näytä pelaajalle kolme vaihtoehtoa ja pyydä pelaajaa valitsemaan yksi niistä
    print("Now you have to choose your next location where you want to go")
    print("Here are your options:")
    print("1. Small airport, from this airport you will get 1 point: ", nearest_small_airport[0][2], ",", nearest_small_airport[0][6], ",", "Distance:", nearest_small_airport[1], "km")
    print("2. Medium airport, from this airport you will get 3 points: ", nearest_medium_airport[0][2], ",", nearest_medium_airport[0][6], ",",  "Distance:", nearest_medium_airport[1], "km")
    print("3. Large airport, from this airport you will get 5 points: ", nearest_large_airport[0][2], ",", nearest_large_airport[0][6], ",",  "Distance:", nearest_large_airport[1], "km")

    choice = ''
    while choice not in ['1', '2', '3']:
        choice = input("Please choose an option (1, 2, or 3): ")
        if choice == '1':
            next_airport = nearest_small_airport
            points += 1  # Lisää yksi piste pienestä lentokentästä
        elif choice == '2':
            next_airport = nearest_medium_airport
            points += 3  # Lisää kolme pistettä keskikokoisesta lentokentästä
        elif choice == '3':
            next_airport = nearest_large_airport
            points += 5  # Lisää viisi pistettä isosta lentokentästä
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

        visited_airports.append(next_airport[0][1])

        print("You have chosen to fly to the following airport: ")
        print(next_airport[0][2], ",", next_airport[0][6], "," , next_airport[1],"km")

        random_airport_result = next_airport[0]


    # Laske matkan pituus ja vähennä se akun tilasta
    distance = next_airport[1]  # Oletan, että tämä on matkan pituus
    battery -= randomize_weather(distance)

    # Tulosta jäljellä oleva akun tila ja lentomatka
    if battery <= 0:
        if next_airport[0][3] == "small_airport":
            points -= 1
        elif next_airport[0][3] == "medium_airport":
            points -= 3
        elif next_airport[0][3] == "large_airport":
            points -= 5

        print("Your airplane's battery is empty. The game has ended.")
        print("Your total points are: " + str(points))
        print("Thank you for playing the game!")
        print("Press any key to quit.")
        input()
        exit()


    print("Your airplane's battery has now " + str(battery) + "km left.")

    # Tulosta pelaajan nykyinen pistemäärä
    print("You have now " + str(points) + " points.")

