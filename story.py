
#Pelin aloitus tarina


screen_name = input("Hi there, what is your name?")
airplane_name = input("Hi " + screen_name + ", now you can choose name for your airplane, what would you like to call it?")

story = ("Welcome " + screen_name + ", to the flight adventure!"
         "In this game, you start your journey with your plane " + airplane_name + " from a randomly selected European airport and choose your next destination from three nearby airports."
         "As you travel, you collect points, but remember that your battery consumes energy. "
         "The game ends when the battery is empty. Good luck on your journey and collect as many points as possible!")

print(story)