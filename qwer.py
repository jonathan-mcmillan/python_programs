from random import *
playing = True
while playing:
    secret = randint(1,100)
    guess = 0
    while guess != secret:
        guess = int(raw_input("Guess the number: "))
        if guess> secret:
            print "Too high"
        elif guess < secret:
            print "Too low"
    print "That's it"
    again = raw_input("Play again? ")
    playing = again.strip().lower()[0]=='y'
