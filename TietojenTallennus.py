# Tallennetaan pelaajan lopputiedot tietokantaan,
# niin että ne voi myöhemmin hakea sieltä.



# Yhteys tietokantaan



def save_player_score(screen_name, aircraft_name, final_location, score):
    sql = ("INSERT INTO player_scores (screen_name, aircraft_name, final_location, score) "
           "VALUES (%s, %s, %s, %s)")
    cursor = yhteys.cursor()
    cursor.execute(sql)




screen_name = input("Enter")
aircraft_name = input("Enter")
final_location = ...
score = 0

# Koodin loppuun funktion kutsu, jolla tiedot tallennetaan
save_player_score(screen_name, aircraft_name, final_location, score)