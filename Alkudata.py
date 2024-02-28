# Tallennetaan pelaajan aloitusdata



#Yhteys tietokantaaan






# Funtio, jolla pelaajan aloitusdata tallennetaan tietokantaan
def save_initial_data(start_battery, start_location, screen_name, aircraft_name):
    sql = ("INSERT INTO game (start_battery, start_location, screen_name, aircraft_name)"
           "VALUES (%s,%s,%s,%s)")
    cursor = yhteys.cursor()
    cursor.execute(sql)




    start_battery = 100
    start_location = ...
    screen_name = input("Enter...")
    aircraft_name = input("Enter...")