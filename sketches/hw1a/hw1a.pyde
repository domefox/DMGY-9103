balls = []

def setup():
    size(600, 400)
    background(220)

def draw():
    background(220)
    
    for ball in balls:
        ball.move()
        ball.display()
        ball.check_edges()

def mousePressed():
    # Check if clicked on a ball
    for ball in balls[:]:
        if ball.contains(mouseX, mouseY):
            balls.remove(ball)
            return
    
    # If not, add a new ball
    balls.append(Ball(mouseX, mouseY))

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.diameter = 50
        self.speed_x = random(-5, 5)
        self.speed_y = random(-5, 5)
        self.color = color(random(255), random(255), random(255))
    
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
    
    def display(self):
        fill(self.color)
        ellipse(self.x, self.y, self.diameter, self.diameter)
    
    def check_edges(self):
        if self.x <= self.diameter/2 or self.x >= width - self.diameter/2:
            self.speed_x *= -1
        if self.y <= self.diameter/2 or self.y >= height - self.diameter/2:
            self.speed_y *= -1
    
    def contains(self, px, py):
        d = dist(px, py, self.x, self.y)
        return d < self.diameter/2
