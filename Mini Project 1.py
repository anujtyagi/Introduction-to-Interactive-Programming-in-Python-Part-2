# implementation of card game - Memory

import simplegui
import random
cards = range(8)+ range(8)
exposed = [False]*16
state = 0
counter = 0
grid = []
for i in range(16):
    grid.append((i*50,50+i*50))
# helper function to initialize globals
def new_game():
    global cards,exposed,counter
    random.shuffle(cards)
    exposed = [False]*16
    counter = 0
    state = 0
# define event handlers
def mouseclick(pos):
    global exposed,state,cards,temp,temp1,counter
    if state == 0:
        temp = pos[0]//50
        exposed[temp] = True
        state = 1
    elif state == 1 and exposed[pos[0]//50] ==False:
        temp1 = pos[0]//50
        exposed[temp1] = True
        state = 2
        counter = counter + 1
    elif exposed[pos[0]//50] ==False:
        if cards[temp] != cards[temp1]:
            exposed[temp] = False
            exposed[temp1] = False
        temp = pos[0]//50
        exposed[temp] = True
        state = 1
    
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
    label.set_text("Turns = "+str(counter))
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


# Always remember to review the grading rubric
