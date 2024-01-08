from js import document, console
from random import randint
from pyodide.ffi import create_proxy

console.log("PyScript initialized!")

random_number = randint(1, 100)

guess_field = document.getElementById("guess")
guesses_field = document.getElementById("guesses")
submit_button = document.getElementById("submit")

guesses = 0
guess = 0
game_over = False

def check_guess(*args):
    global guesses, guess, game_over, random_number, submit_button

    try:
        guess = guess_field.value

        if guess == "":
            document.getElementById("hint").innerHTML = "Gib eine Zahl ein!"
            return

        guess = int(guess)

        if game_over:
            random_number = randint(1, 100)
            guesses = 0
            game_over = False
            document.getElementById("guesses").innerHTML = "10/10 Versuche"
            document.getElementById("hint").innerHTML = ""
            submit_button.innerHTML = "Raten!"
            return
        
        if guesses >= 9:
            document.getElementById("guesses").innerHTML = "0/10 Versuche"
            document.getElementById("hint").innerHTML = f"Du hast 10 Versuche gebraucht. Die richtige Zahl war {random_number}"
            submit_button.innerHTML = "Erneut versuchen"
            game_over = True
            return

        if guess == random_number:
            document.getElementById("hint").innerHTML = "Du hast gewonnen!"
            submit_button.innerHTML = "Erneut versuchen"
            game_over = True
        else:
            guesses += 1
            document.getElementById("guesses").innerHTML = f"{10-guesses}/10 Versuche"
            if guess < random_number:
                document.getElementById("hint").innerHTML = "Die Zahl ist zu klein!"
            else:
                document.getElementById("hint").innerHTML = "Die Zahl ist zu groß!"

    except:
        document.getElementById("hint").innerHTML = "Gib eine gültige Zahl zwischen 1 und 100 ein!"

check_guess_proxy = create_proxy(check_guess)

status = document.getElementById("status")
status.style.visibility = "hidden"

submit_button.addEventListener("click", check_guess_proxy)