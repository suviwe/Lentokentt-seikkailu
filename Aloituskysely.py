# Pelin aloitus, jossa pelaajalta kysytään haluaako hän aloittaa uuden pelin
# vai katsoa edellisten pelien tuloksia.
# Pelin voi aloittaa tulosten katsomisen jälkeen painamalla 1 tai lopettaa ohjelman painamalla enteriä.



import mysql.connector

yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="demoprojekti",
    user="root",
    password="K1ss4tjaS11lit",
    autocommit=True
)

# Funktio, joka kysyy pelaajalta, haluaako hän aloittaa uuden pelin vai katsoa pisteet.
def player_choice():
    while True:
        choice = input("Do you want to start a new game (1) or see player scores (2)? ")
        if choice in ["1", "2"]:
            return choice   # Varmistetaan, että pelaaja voi valita vain 1 tai 2
        else:
            print("Please choose 1 or 2.")  # Tulostetaan virhesanoma jos valinta joku muu

# Funktio hakee pistetiedot tietokannasta
def get_scores():
    sql = ("SELECT * FROM player_scores order by score desc limit 3")
    cursor = yhteys.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

# Funktio, joka tulostaa pisteet ja kysyy pelaajalta, haluaako hän aloittaa uuden pelin tai lopettaa ohjelman
def print_scores_and_ask_for_new_game(results):
    while True:
        if results:
            print("Player scores: ")
            for result in results:
                print(f"Username: {result[1]}")
                print(f"Aircraft: {result[2]}")
                print(f"Score: {result[3]}")
                print()  # Tyhjä rivi erottamaan eri pelaajien tulokset toisistaan
            choice = input("Press (1) to start a new game or press enter to quit ")
            if choice == "":
                print("You closed the program.")
                return
            elif choice == "1":
                print("New adventure begins!")
                return
            else:
                print("Invalid choice. Press 1 or enter.")
        else:
            print("No scores saved.")
            return


choice = player_choice() # Kutsutaan player_choice funktiota pelaajan valinnan mukaan

# Jos valinta 2 kutsutaan get_scores ja print_scores_and_ask_for_new_game funktioita
if choice == "2":
    scores = get_scores()
    print_scores_and_ask_for_new_game(scores)
else:
    print("New adventure begins!")  # pelin aloitus