# implementation of card game - Memory

import simplegui
import random
cards = range(8)+ range(8)
exposed = [False]*16
state = 0
counter = 0
grid = []
for i in range(16):
    grid.append((i*50,50+i*50,False))
# helper function to initialize globals
def new_game():
    global cards,exposed
    random.shuffle(cards)
    exposed = [False]*16
# define event handlers
def mouseclick(pos):
    global exposed,state,cards,temp,temp2,counter
    for i in range(16):
        if pos[0] >= grid[i][0] and pos[0]< grid[i][1]:
            if exposed[i] != True:
                exposed[i] = True
                print state
    if state==0:
        temp = i
        state = 1
    elif state == 1:
        counter = counter +1
        temp2 = i
        state = 2
    else:
        if cards[temp2] != cards[temp]:
            exposed[temp2] = False
            exposed[temp] = False
            temp = i
        state = 1
    print temp,state
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global exposed
    for num in range(len(cards)):
        if exposed[num]:
            canvas.draw_text(str(cards[num]), (20+num*50, 60), 40, 'Red')
        else:
            canvas.draw_line((25+num*50,0),(25+num*50,100),44,'green')
    for num in range(len(cards)+1):
        canvas.draw_line((num*50,0),(num*50,100),3,'Orange')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
