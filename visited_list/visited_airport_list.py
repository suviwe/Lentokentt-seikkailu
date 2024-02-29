#visited airport's idents will be collected to this list.
visited_airports = []

# After the first random airport is chosen, append to the list.
random_airport_result = random.choice(airports)
visited_airports.append(random_airport_result[1])


# After the next airport is chosen, append to the list
choice = ''
    while choice not in ['1', '2', '3']:
        choice = input("Please choose an option (1, 2, or 3): ")
        if choice == '1':
            next_airport = nearest_small_airport
            remaining_range = remaining_range_small_ap
            remaining_battery = remaining_battery_small_ap
            points += 1  # Lisää yksi piste pienestä lentokentästä
        elif choice == '2':
            next_airport = nearest_medium_airport
            remaining_range = remaining_range_medium_ap
            remaining_battery = remaining_battery_medium_ap
            points += 3  # Lisää kolme pistettä keskikokoisesta lentokentästä
        elif choice == '3':
            next_airport = nearest_large_airport
            remaining_range = remaining_range_large_ap
            remaining_battery = remaining_battery_large_ap
            points += 5  # Lisää viisi pistettä isosta lentokentästä
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

    visited_airports.append(next_airport[0][1])

# Use the list in this function so that player will not go to an airport, where he/she is visited once.
def nearest_airport(airport, airports, type):
    your_location = (airport[4], airport[5])
    # Poista nykyinen lentokenttä lentokenttälistasta ja lentokentät, jotka ovat samassa maassa
    airports = [a for a in airports if a[0] != airport[0] and a[1] not in visited_airports]
    distances = [(a, geodesic(your_location, (a[4], a[5])).kilometers) for a in airports if a[3] == type]
    nearest_airport = min(distances, key=lambda x: x[1])
    return nearest_airport