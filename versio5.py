import mysql.connector
import random
from geopy.distance import geodesic

yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="demoprojekti",
    user="root",
    password="K1ss4tjaS11lit",
    autocommit=True
)

# Funktio kysyy pelaajalta, haluaako hän aloittaa uuden pelin vai katsoa pisteet.
def player_choice():
    while True:
        choice = input("Do you want to start a new game (1) or see player scores (2)? ")
        if choice in ["1", "2"]:
            return choice   # Varmistetaan, että pelaaja voi valita vain 1 tai 2
        else:
            print("Please choose 1 or 2.")  # Tulostetaan virhesanoma jos valinta joku muu

# Funktio hakee pistetiedot tietokannasta
def get_scores():
    sql = ("SELECT * FROM player_scores ORDER BY score DESC LIMIT 3")
    cursor = yhteys.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

# Funktio tallentaa pelaajan tiedot ja saadut pisteet tietokantaan
def save_player_score(screen_name, aircraft_name, final_location, score):
    sql = ("INSERT INTO player_scores (screen_name, aircraft_name, score, final_location) "
           "VALUES (%s, %s, %s, %s)")
    cursor = yhteys.cursor()
    cursor.execute(sql, (screen_name, aircraft_name, final_location, score))

# Funktio, joka tulostaa pisteet ja kysyy pelaajalta, haluaako hän aloittaa uuden pelin tai lopettaa ohjelman
def print_scores_and_ask_for_new_game(results):
    if results:
        print("Player scores: ")
        for result in results:
            print(f"Username: {result[1]}")
            print(f"Aircraft: {result[2]}")
            print(f"Score: {result[3]}")
            print()  # Tyhjä rivi erottamaan eri pelaajien tulokset toisistaan
    else:
        print("No scores saved.")

    choice = input("Press (1) to start a new game or press enter to quit ")
    if choice == "":
        print("You closed the program.")
        exit()
    elif choice == "1":
        return True
    else:
        print("Invalid choice. Press 1 or enter.")
        return False

choice = player_choice() # Kutsutaan player_choice funktiota pelaajan valinnan mukaan

# Jos valinta 2 kutsutaan get_scores ja print_scores_and_ask_for_new_game funktioita
if choice == "2":
    scores = get_scores()
    if print_scores_and_ask_for_new_game(scores):
        screen_name = input("Hi there, what is your name?")
        airplane_name = input(f"Hi {screen_name}, now you can choose name for your airplane, what would you like to call it?")
else:
    screen_name = input("Hi there, what is your name?")
    airplane_name = input(f"Hi {screen_name}, now you can choose name for your airplane, what would you like to call it?")

print(str("*" * 37)) #tämä tulostaa tähtiä welcome tekstin yläpuolelle

story1 = (" Welcome " + screen_name + ", to the flight adventure!")

story2= ("In this game, you start your journey with your plane " + airplane_name + " from a randomly selected European airport and choose your next destination from three nearby airports.\n\n"
         "You have a full battery at the beginning, which allows you to fly 2000km. "
         "As you travel, you collect points, but remember that your battery consumes energy.\n\n"
         "Additionally, there's a unique challenge – the current weather conditions at your destination will affect your battery's performance. Unfortunately, you have no control over the weather, so plan your flights wisely!\n\n"
         "The game ends when the battery is empty. Good luck on your journey and collect as many points as possible!\n\n")

print(story1)
print(str("*" *37)) #tämä myös tulostaa tähdet welcome tekstin alapuolelle
print(story2)


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



#visited airport's idents will be collected to this list.
visited_airports = []

#nearest_airport funktio etsii ja palauttaa valituista kokoluokista lähimmän lentokentän annetulle lähtöpaikalle.
#def nearest_airport(airport, airports, type):: Funktio alkaa määrittelyllä. Se ottaa kolme parametria: airport (nykyinen lentokenttä), airports (lista kaikista lentokentistä) ja type (haluttu lentokenttätyyppi).

#your_location = (airport[4], airport[5]): Tallentaa nykyisen lentokentän sijainnin (latitude, longitude) muuttujaan your_location.

#airports = [a for a in airports if a[0] != airport[0] and a[1] not in visited_airports]: Suodattaa lentokentät, poistamalla nykyisen lentokentän ja ne, jotka ovat jo vierailtu (jos käytettävissä).
#Tämä jättää listalle vain ne lentokentät, joita ei ole vielä tarkasteltu.

#distances = [(a, geodesic(your_location, (a[4], a[5])).kilometers) for a in airports if a[3] == type]: Laskee etäisyyden jokaisen jäljellä olevan lentokentän sijainnista. Säilyttää tulokset listana, joka sisältää lentokentän ja sen etäisyyden.

#nearest_airport = min(distances, key=lambda x: x[1]): Etsii pienimmän etäisyyden ja siihen liittyvän lentokentän. key-parametri määrittelee, että minimin vertailukohdaksi käytetään etäisyyksiä.
#return nearest_airport: Palauttaa lähimmän lentokentän ja siihen liittyvän etäisyyden. Tulos on tuple, jossa ensimmäinen arvo on lentokenttä ja toinen arvo on etäisyys.

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
        print(f"The weather is little foggy,so you used 25% more battery.")
    elif result == "rainy":
        new_gap = (gap * 1.50)
        print(f"The weather at your destination is rainy, sorry to say but you used 50% more battery.")
    elif result == "stormy":
        new_gap = (gap * 2)
        print(f"OH NO, The weather is stormy, so your plane will you use 100% more battery.")
    return new_gap

airports = random_airport() #kutsuu funktion random_airports
random_airport_result = random.choice(airports) #funktio random.choice valitsee satunnaisesti yhden lentokenttätiedon airports-listalta
# After the first random airport is chosen, append to the visited list.
visited_airports.append(random_airport_result[1]) #valittu lentokenttä tallennetaan muuttujaan rnadom_airport_result

print("You will start your game at the following airport: ")
print(random_airport_result[2], ",", random_airport_result[6])


nearest_small_airport = nearest_airport(random_airport_result, airports, 'small_airport')
nearest_medium_airport = nearest_airport(random_airport_result, airports, 'medium_airport')
nearest_large_airport = nearest_airport(random_airport_result, airports, 'large_airport')



# Näytä pelaajalle kolme vaihtoehtoa ja pyydä pelaajaa valitsemaan yksi niistä
print("Now you have to choose your next location where you want to go:")
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

visited_airports.append(next_airport[0][1]) # tämä lisää next_airport muuttujan ensimmäisen lentokentän koodin visited_airports-listaan



print("You have chosen to fly to the following airport: ")
print(next_airport[0][2], ",", next_airport[0][6], "," , next_airport[1],"km")


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
    print("Your total points are: " + str(points))
    print("Thank you for playing the game!")
    print("Press any key to quit.")
    input()
    exit()

# Tulosta jäljellä oleva akun tila ja lentomatka
print("Your airplane's battery has now " + str(battery) + "km left.")

# Tulosta pelaajan nykyinen pistemäärä
print("You have now " + str(points) + " points. \n\n")

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
    distance = next_airport[1]
    battery -= randomize_weather(distance)

    # Tarkista, onko pelaajan valitsema kohde sellaisen matkan päässä, jonne akku riittää
    if battery < 0:
        print("Your battery became empty on the way. You didn't reach your selected destination.")
        print("Returning to the previous airport.")
        battery = 0
    else:
        # Jos pelaajan valitsema kohde on saavutettavissa, päivitä final_location valitun lentokentän nimeksi
        final_location = next_airport[0][2]  # Lentokentän nimi

    # Tulosta jäljellä oleva akun tila ja lentomatka
    if battery <= 0:
        if next_airport[0][3] == "small_airport":
            points -= 1
        elif next_airport[0][3] == "medium_airport":
            points -= 3
        elif next_airport[0][3] == "large_airport":
            points -= 5

        print("Your airplane's battery is empty. The game has ended.") # Jos lentokenttää ei enää saavutettu
        print("Your total points are: " + str(points))
        # Tallenna pelaajan pisteet tietokantaan pelin lopussa
        save_player_score(screen_name, airplane_name, points, final_location)

        print("Thank you for playing the game!")
        print("Press any key to quit.")
        input()
        exit()

    print("Your airplane's battery has now " + str(battery) + "km left.")

    # Tulosta pelaajan nykyinen pistemäärä
    print("You have now " + str(points) + " points. \n\n")