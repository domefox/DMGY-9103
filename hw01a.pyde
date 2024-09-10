import random # need this for pyton

# class for agents
class Agent:
    # constructor to set initial agent values
    def __init__(self): # defines constructor class
        self.x = random.uniform(17, width - 17)
        self.y = random.uniform(17, height - 17)
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])
        self.radius = random.uniform(8, 16)
        self.diam = 2 * self.radius

    # update agent position
    def update(self):
        # update position
        self.update_by_velocity()
        #self.update_random()
        #self.update_nearest()

        # check boundary
        self.bounce_boundary()
        #self.wrap_boundary()
        #self.reset_boundary()

    # if agent gets to the edges, bounce back
    def bounce_boundary(self):
        if self.x + self.radius >= width or self.x - self.radius <= 0:
            self.vx *= -1
        if self.y + self.radius >= height or self.y - self.radius <= 0:
            self.vy *= -1

    # if agent gets to the edges, wrap around to the opposite edge. don't need <>0 because Python always returns positive
    def wrap_boundary(self):
        self.x = self.x % width
        self.y = self.y % height

    # if agent gets to the edges, reset it's position, velocity, etc
    def reset_boundary(self):
        if self.x > width or self.x < 0 or self.y > height or self.y < 0:
            self.x = random.uniform(17, width - 17)
            self.y = random.uniform(17, height - 17)
            self.vx = random.choice([-2, -1, 1, 2])
            self.vy = random.choice([-2, -1, 1, 2])
            self.radius = random.uniform(8, 16)
            self.diam = 2 * self.radius

    # use velocity values to update position
    def update_by_velocity(self):
        self.x += self.vx
        self.y += self.vy

    # use random velocity values to update position
    def update_random(self):
        self.vx = random.choice([-3, -2, -1, 1, 2, 3])
        self.vy = random.choice([-3, -2, -1, 1, 2, 3])
        self.x += self.vx
        self.y += self.vy

    def dist_comp(self, agentA, agentB):
        distA = dist(self.x, self.y, agentA.x, agentA.y)
        distB = dist(self.x, self.y, agentB.x, agentB.y)
        return distA - distB

    # move away from nearest agent
    def update_nearest(self):
        sorted_by_dist = sorted(agents, key=lambda agent: dist(self.x, self.y, agent.x, agent.y))
        closest_agent = sorted_by_dist[1]  # [0] would be self
        self.vx = map(closest_agent.x - self.x, -width, width, 4, -4)
        self.vy = map(closest_agent.y - self.y, -height, height, 4, -4)
        self.x += self.vx
        self.y += self.vy

    # draw agent
    def draw_agent(self):
        ellipse(self.x, self.y, self.diam, self.diam)

    # draw based on currentMode
    def draw(self):
        if current_mode == POINT_MODE:
            stroke(0)
            self.draw_point()
        elif current_mode == FURTHEST_MODE:
            stroke(0, 8)
            self.draw_furthest()
        elif current_mode == NEAREST_MODE:
            stroke(0, 8)
            self.draw_nearest()
        elif current_mode == OVERLAP_MODE:
            stroke(0, 16)
            noFill()
            self.draw_overlap()

    # draw black point at x, y
    def draw_point(self):
        point(self.x, self.y)

    # draw a line between each agent and the agent furthest away from it
    def draw_furthest(self):
        sorted_by_dist = sorted(agents, key=lambda agent: dist(self.x, self.y, agent.x, agent.y))
        furthest_agent = sorted_by_dist[-1]
        line(self.x, self.y, furthest_agent.x, furthest_agent.y)

    # draw a line between each agent and its nearest agent
    def draw_nearest(self):
        sorted_by_dist = sorted(agents, key=lambda agent: dist(self.x, self.y, agent.x, agent.y))
        nearest_agent = sorted_by_dist[1]  # [0] would be self
        line(self.x, self.y, nearest_agent.x, nearest_agent.y)

    # draw ellipse between agents when they overlap
    def draw_overlap(self):
        for other_agent in agents:
            if self != other_agent:
                t_dist = dist(self.x, self.y, other_agent.x, other_agent.y)
                if t_dist < self.radius + other_agent.radius:
                    cx = (self.x + other_agent.x) / 2
                    cy = (self.y + other_agent.y) / 2
                    ellipse(cx, cy, t_dist, t_dist)

# max number of agents
max_agents = 32

# array for keeping track of agents
agents = []

# keep track of current mode
AGENT_MODE = 0
POINT_MODE = 1
FURTHEST_MODE = 2
NEAREST_MODE = 3
OVERLAP_MODE = 4

current_mode = AGENT_MODE

def setup():
    global agents
    size(1200, 800)  # Adjust as needed, Processing Python doesn't have windowWidth/Height

    # set initial state
    global current_mode
    current_mode = AGENT_MODE

    # create agents and store them in array
    for _ in range(max_agents):
        agents.append(Agent())

def draw():
    global agents, current_mode

    # update agents
    for agent in agents:
        agent.update()

    # depending on the mode:
    if current_mode == AGENT_MODE:
        background(220, 20, 120)

        # draw agents
        noStroke()
        fill(255)
        for agent in agents:
            agent.draw_agent()
    else:
        for agent in agents:
            agent.draw()

def mouseClicked():
    global current_mode
    # cycle through modes
    current_mode = (current_mode + 1) % 5
    if current_mode != AGENT_MODE:
        background(255)

def keyReleased():
    global current_mode
    # if drawing:
    if current_mode != AGENT_MODE:
        # s: save drawing
        if key == 's' or key == 'S':
            saveFrame("my-drawing.jpg")

        # r: reset
        if key == 'r' or key == 'R':
            background(255)
