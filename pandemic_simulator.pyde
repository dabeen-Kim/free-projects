###########################
# Created by: Dabeen Kim
# Date: 2021.02.24
# Reference: "Pandemic simulation" https://www.youtube.com/watch?v=oLvhAfOZSEo
# Dependency: Processing, Python3
w = 1000
h = 600
timer = 0

people_num = 200        # total people number
psize = 3               # person size / 2

infection_prob = 0.7     # virus infection probability
recovery_prob = 0.3      # recovery probability
death_prob = 0.05        # death probability

# status dictionary. it contains status, color, and current people's number for each status.
status_dict = {
               "normal" : [color(255, 255, 255), people_num-1],
               "infected" : [color(255, 0, 0), 1],
               "recovered" : [color(0, 255, 255), 0],
               "dead" : [color(0, 0, 0), 0]
               }

# PERSON CLASS
# [variables]
# status: current person state. for example, status wound be "infected" if a person did.
#         each status has designated color.
# c : color.
# counter : if a person is infected, this variable is decreased so infection state will be lasted at least 5 second.
#           you can change this time whatever you want.
# x, y : person's current position.
# dx, dy : person's direction and speed.

# [methods]
# changePos(): change person position.
# checkDist(another_person): calculate the distance between this person and another person.
# change_status(new_status, probability): change current status to new_status. it will be changed
#                                         depending on the probability.
# recover_or_dead(): change infected person's status, recover or dead. it is determined randomly.
# display(): display person with the designated color.
class Person:
    def __init__(self, status, width, height):
        self.status = status
        self.c = status_dict[status][0]
        self.counter = int(random(5, 10)) * 60
        self.x = random(psize, width-psize)
        self.y = random(psize, height-psize)
        self.dx = random(-2, 2)
        self.dy = random(-2, 2)
    
    def changePos(self):
        if self.x <= psize or self.x >= width-psize:
            self.dx *= -1
        if self.y <= psize or self.y >= height-psize:
            self.dy *= -1
            
        self.x += self.dx
        self.y += self.dy
    
    def checkDist(self, person):
        if (self.status == "normal" and person.status == "infected") or \
            (self.status == "infected" and person.status == "normal"):
            xdiff = abs(self.x - person.x)
            ydiff = abs(self.y - person.y)
            return sqrt(xdiff**2 + ydiff**2)
        else:
            return int(1e3)
    
    def change_status(self, newstatus, prob):
        if random(0, 1) <= prob:
            status_dict[self.status][1] -= 1
            self.status = newstatus
            status_dict[newstatus][1] += 1
            self.c = status_dict[newstatus][0]
    
    def recover_or_dead(self):
        if random(0, 1) < 0.5:
            self.change_status("recovered", recovery_prob)
        else:
            self.change_status("dead", death_prob)
            
    def display(self):
        if self.status != "dead":
            self.changePos()
        fill(self.c)
        ellipse(self.x, self.y, psize*2, psize*2)

People = []
for _ in range(people_num-1):
    People.append(Person("normal", w, h))
People.append(Person("infected", w, h))

def setup():
    size(w, h)
    noStroke()
    textSize(15)

def draw():
    global timer
    background(150)
    
    # check people distances for 6 times per 1 second.
    # if you want to change check rate, change below number.
    if timer % 10 == 0:
        for i in range(people_num-1):
            for j in range(i+1, people_num):
                d = People[i].checkDist(People[j])
                if d <= psize*2 + 4:
                    if People[i].status == "normal":
                        People[i].change_status("infected", infection_prob)
                    else:
                        People[j].change_status("infected", infection_prob)
    timer = (timer + 1) % 60
    
    # change infected person's status and visualize people
    for person in People:
        if person.status == "infected":
            if person.counter <= 0:
                person.recover_or_dead()
            else:
                person.counter -= 1
        person.display()
    
    # print current people status
    i = 14
    for s, (c, num) in status_dict.items():
        fill(c)
        text(s.upper()+": "+str(num), 10, i)
        i += 14
