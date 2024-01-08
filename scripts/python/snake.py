from js import document, setInterval, console, Audio
from pyodide.ffi import create_proxy
from random import randint

console.log("PyScript initialized!")

SPEED = 100

class Canvas:
	def __init__(self, id: str):
		canvas = document.getElementById(id)
		self.ctx = canvas.getContext("2d")
		self.snakePosition = [0, 0]
		self.width = canvas.width
		self.height = canvas.height
	
	def clear(self): # Leert den Canvas
		self.ctx.clearRect(0, 0, canvas.width, canvas.height)

	def draw(self, x, y, color="green", width=16, height=16): # Zeichnet ein Rechteck
		self.ctx.fillStyle = color
		self.ctx.fillRect(x, y, width, height)

	def draw_text(self, text, x, y, size=16, color="white", font="Arial"): # Zeigt Text an
		self.ctx.fillStyle = color
		self.ctx.font = f"{size}px {font}"
		self.ctx.fillText(text, x, y)

	def random_position(self): # Generiert eine zufällige Position auf dem Canvas
		x = round(randint(0, (canvas.width - 16) // 16) * 16)
		y = round(randint(0, (canvas.height - 16) // 16) * 16)
		return {"x": x, "y": y}

canvas = Canvas("canvas")

class Food:
	def __init__(self):
		self.position = canvas.random_position()

	def regenerate(self): # Regeneriert das Essen
		self.position = canvas.random_position()

	def draw(self): # Zeichnet das Essen
		canvas.draw(self.position["x"], self.position["y"], "red")

class Snake:
	def __init__(self):
		self.snakeBody = [{"x": 64, "y": 64}]
		self.direction = "right"
		self.food = Food()
		self.game_over = False
		self.food.regenerate()

	def move(self, direction): # Bewegt die Schlange
		if self.game_over:
			self.game_over = False

		if direction in ["a", "d", "w", "s"]:
			opposite_directions = {"a": "d", "d": "a", "w": "s", "s": "w"}
			if (not self.game_over and direction != opposite_directions.get(self.direction))\
				or len(self.snakeBody) <= 2:
					self.direction = direction

	def updatePosition(self): # "Wandelt" die Eingabe zu Koordinaten um
		head = self.snakeBody[0].copy()
		if self.direction == "a":
			head["x"] -= 16
		elif self.direction == "d":
			head["x"] += 16
		elif self.direction == "w":
			head["y"] -= 16
		elif self.direction == "s":
			head["y"] += 16
		self.snakeBody.insert(0, head)
		self.snakeBody.pop()

	def grow(self): # Fügt der Schlange ein Segment hinzu
		new_segment = self.snakeBody[-1].copy()
		self.snakeBody.append(new_segment)

	def checkBounds(self): # Prüft ob die Schlange innerhalb des Canvas liegt
		head = self.snakeBody[0]
		if head["x"] >= canvas.width or head["x"] < 0 or head["y"] >= canvas.height or head["y"] < 0:
			self.gameOver()

	def checkCollision(self): # Prüft ob die Schlange mit etwas kollidiert
		head = self.snakeBody[0]
		
		for segment in self.snakeBody[1:]:
			if segment == head:
				self.gameOver()
				break
		
		if head == self.food.position:
			sound_eat.play()
			self.grow()
			self.food.regenerate()

	def gameOver(self): # Beendet das Spiel
		self.game_over = True
		self.snakeBody = [{"x": 64, "y": 64}]
		self.food.regenerate()

		sound_game_over.play()

		game_over_text = "Game over!"
		font_size = 32

		canvas.clear()
		canvas.draw_text(game_over_text, (canvas.width - (len(game_over_text) // 2) * font_size) // 2, canvas.height // 2, font_size, "red")

	def update(self): # Game Loop
		if self.game_over:
			return
		else:
			canvas.clear()
		
		self.updatePosition()
		self.checkCollision()
		self.checkBounds()

		for part in self.snakeBody:
			canvas.draw(part["x"], part["y"])

		self.food.draw()

		canvas.draw_text("Score: " + str(len(self.snakeBody) - 1), 16, 32)

sound_eat = Audio.new("../audio/food_eaten.wav")
sound_game_over = Audio.new("../audio/game_over.wav")

snake = Snake()

def move(event):
	snake.move(event.key)

def main():
	document.addEventListener("keypress", create_proxy(move)) # Zeichnet Tastendrücke auf
	setInterval(create_proxy(snake.update), SPEED) # Startet den Game Loop mit einem Interval, der die Spielgeschwindigkeit bestimmt

main()