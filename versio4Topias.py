import mysql.connector
import random
from geopy.distance import geodesic
import keyboard


yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port=3306,
         database='lentokenttäpeli',
         user='root',
         password='ulluas3156',
         autocommit=True
         )

#funktio hakee ja palauttaa tietokannasta Euroopassa olevat kentät, rajaten tulokset isoihin,keskikokoisiin ja pieniin.
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

#nearest_airport funktio etsii ja palauttaa valituista kokoluokista lähimmän lentokentän annetulle lähtöpaikalle.
#def nearest_airport(airport, airports, type):: Funktio alkaa määrittelyllä. Se ottaa kolme parametria: airport (nykyinen lentokenttä), airports (lista kaikista lentokentistä) ja type (haluttu lentokenttätyyppi).

#your_location = (airport[4], airport[5]): Tallentaa nykyisen lentokentän sijainnin (latitude, longitude) muuttujaan your_location.

#airports = [a for a in airports if a[0] != airport[0] and a[1] not in visited_airports]: Suodattaa lentokentät, poistamalla nykyisen lentokentän ja ne, jotka ovat jo vierailtu (jos käytettävissä).
#Tämä jättää listalle vain ne lentokentät, joita ei ole vielä tarkasteltu.

#distances = [(a, geodesic(your_location, (a[4], a[5])).kilometers) for a in airports if a[3] == type]: Laskee etäisyyden jokaisen jäljellä olevan lentokentän sijainnista. Säilyttää tulokset listana, joka sisältää lentokentän ja sen etäisyyden.

#nearest_airport = min(distances, key=lambda x: x[1]): Etsii pienimmän etäisyyden ja siihen liittyvän lentokentän. key-parametri määrittelee, että minimin vertailukohdaksi käytetään etäisyyksiä.
#return nearest_airport: Palauttaa lähimmän lentokentän ja siihen liittyvän etäisyyden. Tulos on tuple, jossa ensimmäinen arvo on lentokenttä ja toinen arvo on etäisyys.'''
def nearest_airport(airport, airports, type):
    your_location = (airport[4], airport[5])
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
        print("The weather is clear. Keep on going, enjoy the trip!")
    elif result == "foggy":
        new_gap = (gap * 1.25)
        print(f"The weather is a little foggy, so you used 25% more battery.")
    elif result == "rainy":
        new_gap = (gap * 1.50)
        print(f"The weather at your destination is rainy, sorry to say but you used 50% more battery.")
    elif result == "stormy":
        new_gap = (gap * 2)
        print(f"OH NO, The weather is stormy, so your plane will use 100% more battery.")
    return new_gap

# Initialize the game
def initialize_game():
    screen_name = input("Hi there, what is your name? ")
    airplane_name = input(f"Hi {screen_name}, now you can choose a name for your airplane. What would you like to call it? ")
    return screen_name, airplane_name, 2000, 0, []

# Welcome message
def print_welcome_message(airplane_name):
    print("*" * 37)
    print(f"{' Welcome ':^37}")
    print("*" * 37)
    print(f"In this game, you start your journey with your plane {airplane_name} from a randomly selected European airport and choose your next destination from three nearby airports.\n"
          "You have a full battery at the beginning, which allows you to fly 2000km. "
          "As you travel, you collect points, but remember that your battery consumes energy.\n"
          "Additionally, there's a unique challenge – the current weather conditions at your destination will affect your battery's performance. Unfortunately, you have no control over the weather, so plan your flights wisely!\n"
          "The game ends when the battery is empty. Good luck on your journey and collect as many points as possible!\n")

# Main game loop
while True:
    screen_name, airplane_name, battery, points, visited_airports = initialize_game()
    print_welcome_message(airplane_name)

    while battery > 0:
        #kutsuu funktion random_airports
        airports = random_airport()
        random_airport_result = random.choice(airports) #funktio random.choice valitsee satunnaisesti yhden lentokenttätiedon airports-listalta
        visited_airports.append(random_airport_result[1]) #valittu lentokenttä tallennetaan muuttujaan rnadom_airport_result

        print(f"You will start your game at the following airport: {random_airport_result[2]}, {random_airport_result[6]}")

        nearest_small_airport = nearest_airport(random_airport_result, airports, 'small_airport')
        nearest_medium_airport = nearest_airport(random_airport_result, airports, 'medium_airport')
        nearest_large_airport = nearest_airport(random_airport_result, airports, 'large_airport')

        # Näytä pelaajalle kolme vaihtoehtoa ja pyydä pelaajaa valitsemaan yksi niistä
        print("Now you have to choose your next location where you want to go:")
        print("Here are your options:")
        print("1. Small airport, from this airport you will get 1 point:", nearest_small_airport[0][2], ",", nearest_small_airport[0][6], ", Distance:", nearest_small_airport[1], "km")
        print("2. Medium airport, from this airport you will get 3 points:", nearest_medium_airport[0][2], ",", nearest_medium_airport[0][6], ", Distance:", nearest_medium_airport[1], "km")
        print("3. Large airport, from this airport you will get 5 points:", nearest_large_airport[0][2], ",", nearest_large_airport[0][6], ", Distance:", nearest_large_airport[1], "km")

        choice = ''
        while choice not in ['1', '2', '3']:
            choice = input("Please choose an option (1, 2, or 3): ")
            if choice == '1':
                next_airport = nearest_small_airport
                points += 1
            elif choice == '2':
                next_airport = nearest_medium_airport
                points += 3
            elif choice == '3':
                next_airport = nearest_large_airport
                points += 5
            else:
                print("Invalid choice. Please choose 1, 2, or 3.")

        visited_airports.append(next_airport[0][1])

        print(f"You have chosen to fly to the following airport: {next_airport[0][2]}, {next_airport[0][6]}, Distance: {next_airport[1]} km")

        distance = next_airport[1]
        battery -= randomize_weather(distance)

        if battery <= 0:
            if next_airport[0][3] == "small_airport":
                points -= 1
            elif next_airport[0][3] == "medium_airport":
                points -= 3
            elif next_airport[0][3] == "large_airport":
                points -= 5

            print("Your airplane's battery is empty. The game has ended.")
            print(f"Your total points are: {points}")
            break

        # Tulosta jäljellä oleva akun tila ja lentomatka
        print(f"Your airplane's battery has now {battery} km left.")
        # Tulosta pelaajan nykyinen pistemäärä
        print(f"You have now {points} points.\n")

        # Jos esc-nappia painetaan peli loppuu
        if keyboard.is_pressed('esc'):
            print("Starting a new game...")
            break
    # pelin loputtua kysyy haluuako pelaaja aloittaa pelin uudelleen
    play_again = input("Do you want to play again? (yes/no): ").strip().lower()
    if play_again != 'yes':
        print("Thank you for playing the game!")
        break
