import numpy
import numpy.core._methods
import numpy.lib.format
import pygame
from pygame.locals import *
from pygame.mixer import *
from pygame.image import *
from tkinter import *
from tkinter import filedialog

def solve_start():
    global squares
    global unitlist
    global units
    global peers
    global digits
    
    digits   = '123456789'
    rows     = 'ABCDEFGHI'
    cols     = digits

    squares  = cross(rows, cols)

    unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

    units = dict((s, [u for u in unitlist if s in u]) 
             for s in squares)

    peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

def grid_values(grid):
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

def parse_grid(grid):
    values = dict((s, digits) for s in squares) #At start each cell may take any digit
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False 
    return values

def assign(values, s, d):
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    #cou=1
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d,'')
    
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        r = ord(s[0]) - 64
        c = int(s[1])
        grid_vals[r - 1][c - 1] = int(d2)
        img = pygame.image.load(str(int(grid_vals[r-1][c-1])) + "_act.jpg")
        img = pygame.transform.scale(img, (26,24))
        box_y = back_img.get_height()/2 - 128 + (r-1)*30 + (r-1)*2
        if (c-1)==0:
            box_x = back_img.get_width()/2 - 142 + (c-1)*33
        else:
            box_x = back_img.get_width()/2 - 142 + (c-1)*33 - 2
        screen.blit(img,(box_x,box_y))
        pygame.time.wait(50)
        pygame.display.update()
        #pygame.time.wait(50)
        #print(cou)
        #cou=cou+1
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False 
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values

def solve(grid): 
    return search(parse_grid(grid))

def search(values):
    if values is False:
        return False 
    if all(len(values[s]) == 1 for s in squares): 
        return values 
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])

def some(seq):
    for e in seq:
        if e: return e
    return False

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def button_function(button):
    global present_state
    global x_fill
    global y_fill
    global grid_vals
    global previous_state
    global solved
    global gameExit
    if button == "quit_":
        previous_state = present_state
        present_state = "Quit_screen"
        #print(present_state)
        quit_screen()
    elif button == "options_":
        present_state = "Option_screen"
    elif button == "start_":
        #grid = ""
        solved = 0
        solve_start()
        present_state = "Game_Screen"
        grid_vals = numpy.zeros((9,9))
    elif button == "yes_":
        pygame.quit() 
        gameExit = True
        quit()
    elif button == "no_":
        if present_state == "Quit_screen":
            present_state = previous_state
    elif button == "back_" or button == "back_or_":
        if present_state == "Option_screen":
            present_state = "Main_Menu"
        elif present_state == "Game_Screen":
            present_state = "Main_Menu"
            x_fill = 0
            y_fill = 0
            grid_vals = numpy.zeros((9,9))
            grids = ""
    elif button == "solve_":
        solved = 1
        grid_form()
    elif button == "reset_":
        x_fill = 0
        y_fill = 0
        grid_vals = numpy.zeros((9,9))
        grids = ""
        solved = 0
    elif button == "save_":
        save_file()
    elif button == "load_":
        load_file()

def save_file():
    global grids
    global saved
    if saved == 0:
        root = Tk()
        root.withdraw()
        root.filename =  filedialog.asksaveasfilename(defaultextension='.txt', filetypes = (("Text Files","*.txt"),))
        if not root.filename == "": 
            file = open(root.filename,"w")
            file.write(grids)
            file.close()
        root.destroy()
        pygame.mouse.set_pos(back_img.get_width(),back_img.get_height())
    saved = 1
    #root.destroy()

def load_file():
    global loaded
    global solved
    if loaded == 0:
        root = Tk()
        root.withdraw()
        root.fileName = filedialog.askopenfilename(filetypes = (("Text Files", "*.txt"),))
        if not root.fileName == "":
            file = open(root.fileName,"r")
            contents = file.read()
            file.close()
            if not contents == "":
                #print(len(contents))
                load_grid(contents)
            else:
                #print("Empty!")
                s = "0"*81
                load_grid(s)
        root.destroy()
        pygame.mouse.set_pos(back_img.get_width(),back_img.get_height())
    loaded = 1
    solved = 0

def grid_form():
    global grids
    grids = ""
    for i in range(0,9):
        for j in range(0,9):
            grids = grids + str(int(grid_vals[i][j]))
    solve(grids)
    #print(grid)

def save_grid():
    global grids
    grids = ""
    for i in range(0,9):
        for j in range(0,9):
            grids = grids + str(int(grid_vals[i][j]))

def load_grid(sent):
    global grids
    global grid_vals
    grids = sent
    cc = 0
    for i in range(0,9):
        for j in range(0,9):
            grid_vals[i][j] = int(grids[cc])
            cc = cc+1

def button_display(cur_pos, button, disp_pos, but_size):
    global loaded
    global saved
    if not ((disp_pos[0] < cur_pos[0] < disp_pos[0]+but_size[0]) and (disp_pos[1] < cur_pos[1] < disp_pos[1]+but_size[1])):
        butt_img = pygame.image.load(button+"nor.jpg")
        butt_img = pygame.transform.scale(butt_img,but_size)
        screen.blit(butt_img, disp_pos)
    elif not(pygame.mouse.get_pressed()[0]):
        butt_img = pygame.image.load(button+"hov.jpg")
        butt_img = pygame.transform.scale(butt_img,but_size)
        screen.blit(butt_img, disp_pos)
    else:
        butt_img = pygame.image.load(button+"pre.jpg")
        butt_img = pygame.transform.scale(butt_img,but_size)
        screen.blit(butt_img, disp_pos)
        button_function(button)

def main_screen():
    screen.blit(BackGround.image, BackGround.rect)
    button_display(cur_pos,start_,but_pos,but_size)
    button_display(cur_pos,options_,(but_pos[0],but_pos[1]+60),but_size)
    button_display(cur_pos,quit_,(but_pos[0]+20,but_pos[1]+120),(but_size[0]-40,but_size[1]))
    pygame.display.update()

def slider():
    global vol
    white  = (255,255,255)
    black = (0,0,0)
    pygame.draw.rect(screen, white, [back_img.get_width()/2 - 30, back_img.get_height()/2 - 5, 200, 10])
    pygame.draw.circle(screen, white, (int(back_img.get_width()/2 - 30), int(back_img.get_height()/2)), 5, 2)
    pygame.draw.circle(screen, white, (int(back_img.get_width()/2 +170), int(back_img.get_height()/2)), 5, 2)
    if not (((back_img.get_width()/2 - 35 <= pygame.mouse.get_pos()[0] <= back_img.get_width()/2 + 170) and 
             (back_img.get_height()/2 -30 <= pygame.mouse.get_pos()[1] <= back_img.get_height()/2 +30)) and
            (pygame.mouse.get_pressed()[0])):
        pygame.draw.rect(screen, white, [(back_img.get_width()/2 - 35)+int(2*vol*100), back_img.get_height()/2 - 10, 10, 20])
        pygame.draw.rect(screen, black, [(back_img.get_width()/2 - 35)+int(2*vol*100), back_img.get_height()/2 - 10, 10, 20], 1)
    elif (((back_img.get_width()/2 - 35 < pygame.mouse.get_pos()[0] < back_img.get_width()/2 + 170) and
           (back_img.get_height()/2 -30 < pygame.mouse.get_pos()[1] < back_img.get_height()/2 +30)) and
            (pygame.mouse.get_pressed()[0])):
        pygame.draw.rect(screen, white, [pygame.mouse.get_pos()[0], back_img.get_height()/2 - 10, 10, 20])
        pygame.draw.rect(screen, black, [pygame.mouse.get_pos()[0], back_img.get_height()/2 - 10, 10, 20], 1)
        vol = (pygame.mouse.get_pos()[0] - (back_img.get_width()/2 - 30))/200

def digits_img():
    global dig_act_arr
    global dig_inact_arr
    dig_act_arr = []
    dig_inact_arr = []
    for i in range(0,9):
        dig_act_arr.append(pygame.image.load(str(i+1)+"_act.jpg"))
        dig_act_arr[i] = pygame.transform.scale(dig_act_arr[i],(40,40))
        dig_inact_arr.append(pygame.image.load(str(i+1)+"_inact.jpg"))
        dig_inact_arr[i] = pygame.transform.scale(dig_inact_arr[i],(40,40))

def display_dig(flag,row,col):
    global x_fill
    global y_fill
    global grid_vals
    global vals
    dig_arr = dig_inact_arr
    for i in range(0,9):
        if flag == 1:
            act = 0
            for j in vals:
                if (i+1 == j):
                    act = 1
            if act == 1:
                screen.blit(dig_act_arr[i], (back_img.get_width()/2 - 200 + i*45, back_img.get_height()/2 + 195))
            else:
                screen.blit(dig_inact_arr[i], (back_img.get_width()/2 - 200 + i*45, back_img.get_height()/2 + 195))
            if not row == -1:
                #if i+1 != 
                if ((back_img.get_width()/2 - 200 + i*45 <= pygame.mouse.get_pos()[0] <= back_img.get_width()/2 - 200 + i*45 + 40) and
                    (back_img.get_height()/2 + 195 <= pygame.mouse.get_pos()[1] <= back_img.get_height()/2 + 195 + 40) and
                    (pygame.mouse.get_pressed()[0] == 1)):
                    if act == 1:
                    #screen.blit(dig_arr[i], (x_fill, y_fill))
                        grid_vals[row][col] = i+1
                        dig_arr = dig_inact_arr
                        x_fill = 0
                        y_fill = 0
                        vals = [1,2,3,4,5,6,7,8,9]
        else:
            screen.blit(dig_arr[i], (back_img.get_width()/2 - 200 + i*45, back_img.get_height()/2 + 195))
    clr = pygame.image.load("clear.jpg")
    clr = pygame.transform.scale(clr,(40,40))
    screen.blit(clr, (back_img.get_width()/2 - 200 + (i+1)*45, back_img.get_height()/2 + 195))
    if ((back_img.get_width()/2 - 200 + (i+1)*45 <= pygame.mouse.get_pos()[0] <= back_img.get_width()/2 - 200 + (i+1)*45 + 40) and
        (back_img.get_height()/2 + 195 <= pygame.mouse.get_pos()[1] <= back_img.get_height()/2 + 195 + 40) and
        (pygame.mouse.get_pressed()[0] == 1)):
        if flag == 1:
            grid_vals[row][col] = 0
        #pygame.display.update()

def unit_check(row,col):
    global grid_vals
    global vals
    r=1
    for i in range (0, 9):
        if i==row:
            continue
        else:
            if not int(grid_vals[i][col]) == 0:
                for n in vals:
                    if n == grid_vals[i][col]:
                        vals.remove(int(grid_vals[i][col]))
    for j in range(0, 9):
        if j==col:
            continue
        else:
            if not int(grid_vals[row][j]) == 0:
                for n in vals:
                    if n == grid_vals[row][j]:
                        vals.remove(int(grid_vals[row][j]))
    i = int(row/3) * 3
    j = int(col/3) * 3
    for k in range(i,i+3):
        for l in range(j, j+3):
            if k == row and l == col:
                continue
            else:
                if not (int(grid_vals[k][l]) == 0):
                    for n in vals:
                        if n == grid_vals[k][l]:
                            vals.remove(int(grid_vals[k][l]))
def game_screen():
    global x_fill
    global y_fill
    global grid_vals
    global vals
    global solved
    #normal_fill = (249, 241, 217)
    activated_fill = (240,162,103)
    cursor = pygame.mouse.get_pos()
    isPressed = pygame.mouse.get_pressed()[0]
    back_ground = pygame.image.load("Game_screen.jpg")
    back_ground = pygame.transform.scale(back_ground, (back_img.get_width(), back_img.get_height()))
    title = pygame.image.load("sudoku_solver.jpg")
    title = pygame.transform.scale(title, (180, 80))
    grid = pygame.image.load("Grid.jpg")
    grid = pygame.transform.scale(grid, (350, 350))
    screen.blit(back_ground, (0,0))
    screen.blit(grid, (back_img.get_width()/2 - 175, 86))
    screen.blit(title, (back_img.get_width()/2 - 90, 0))
    button_display(cur_pos, "back_or_", (0, back_img.get_height() - 30), (90, 30))
    button_display(cur_pos, "load_",(20, back_img.get_height()/2 - 70), (120, 50))
    button_display(cur_pos, "save_",(20, back_img.get_height()/2), (120, 50))
    button_display(cur_pos, "reset_",(20, back_img.get_height()/2 + 70), (100, 100))
    if solved == 0:
        button_display(cur_pos, "solve_", (back_img.get_width() - 150, back_img.get_height()/2 - 35), (80, 80))
    else:
        img = pygame.image.load("solve_inact.jpg")
        img = pygame.transform.scale(img, (80,80))
        screen.blit(img, (back_img.get_width() - 150, back_img.get_height()/2 - 25))
    for j in range(0, 9):
        for i in range(0, 9):
            box_y = back_img.get_height()/2 - 128 + j*30 + j*2
            if i==0:
                box_x = back_img.get_width()/2 - 142 + i*33
            else:
                box_x = back_img.get_width()/2 - 142 + i*33 - 2
            if ((box_x <= cursor[0] <= box_x + 26) and (box_y <= cursor[1] <= box_y + 24)) and isPressed == 1:
                vals = [1,2,3,4,5,6,7,8,9]
                x_fill = box_x
                y_fill = box_y
                unit_check(j,i)
                #print(vals)
            if not(x_fill == 0) or not(y_fill == 0):
                pygame.draw.rect(screen, activated_fill, [x_fill, y_fill, 26, 24])
                if box_x == x_fill and box_y == y_fill:
                    display_dig(1,j,i)
                else:
                    display_dig(1,-1,-1)
            else:
                display_dig(0,0,0)
            if not(int(grid_vals[j][i]) == 0):
                img = pygame.image.load(str(int(grid_vals[j][i])) + "_act.jpg")
                img = pygame.transform.scale(img, (26,24))
                screen.blit(img,(box_x,box_y))
            #if not(grid_vals[j][i] == 0):
                #pygame.blit
    #print(vals)
    pygame.display.update()

def option_screen():
    light_orange = (240,162,103)
    screen.fill(light_orange)
    title = pygame.image.load("options.jpg")
    title = pygame.transform.scale(title, (250,80))
    mus_vol = pygame.image.load("Music_Vol.jpg")
    mus_vol = pygame.transform.scale(mus_vol, (200, 60))
    screen.blit(title,((back_img.get_width()/2 - 250/2,back_img.get_height()/2 - 200)))
    screen.blit(mus_vol,((back_img.get_width()/2 - 250,back_img.get_height()/2 - 35)))
    button_display(cur_pos,"back_",(back_img.get_width()/2 - 75, back_img.get_height()/2 + 100),(150, 40))
    slider()
    pygame.display.update()

def quit_screen():
    light_orange = (240,162,103)
    msg = pygame.image.load("r_u_sure.jpg")
    msg = pygame.transform.scale(msg, (350, 80))
    screen.fill(light_orange)
    screen.blit(msg, (back_img.get_width()/2 - 350/2,back_img.get_height()/2 - 100))
    button_display(cur_pos,"no_",(back_img.get_width()/2 + 100, back_img.get_height()/2 + 100),(100, 50))
    button_display(cur_pos,"yes_",(back_img.get_width()/2 - 200, back_img.get_height()/2 + 100), (100, 50))
    if gameExit == False:
        pygame.display.update()
    #print(present_state)

x= pygame.init()
menu_music = pygame.mixer.music.load("Main_Menu.ogg")
pygame.display.set_caption("Sudoku Solver")
back_img =  pygame.image.load("Back.jpg")
start_ = "start_"
options_ = "options_"
quit_ = "quit_"
but_pos = (550,300)
but_size = (150,40)
present_state = "Main_Menu"
previous_state = "Main_Menu"
vol = 0.2
x_fill = 0
y_fill = 0
grids = ""
vals = [1,2,3,4,5,6,7,8,9]
solved = 0
saved = 0
loaded = 0
digits_img()
#start_img = pygame.image.load(os.path.join("textures","start_nor.png"))
#start_img = pygame.transform.scale(button_img,(150,40))
#options_img = pygame.image.load(os.path.join("textures","options_nor.png"))
#options_img = pygame.transform.scale(button_img,(150,40))
#quit_img = pygame.image.load(os.path.join("textures","quit_nor.png"))
#quit_img = pygame.transform.scale(button_img,(150,40))
screen = pygame.display.set_mode((back_img.get_width(),back_img.get_height()))
pygame.mixer.music.play(-1)
BackGround = Background("Back.jpg", [0,0])
#pygame.display.update()
gameExit = False

while gameExit == False:
    #screen.fill([255,255,255])
    global cur_pos
    if gameExit == True:
        break
    cur_pos = pygame.mouse.get_pos()
    pygame.mixer.music.set_volume(vol)
    for event in pygame.event.get():
        #print(pygame.key.get_focused())
        if event.type == pygame.KEYDOWN:
            if event.key == 256:
                pygame.quit()
        if event.type == pygame.QUIT:
            button_function("quit_")
    if present_state == "Main_Menu":
        main_screen()
        #pygame.display.toggle_fullscreen()
    elif present_state == "Option_screen":
        option_screen()
    elif present_state == "Quit_screen":
        quit_screen()
    elif present_state == "Game_Screen":
        game_screen()
    #screen.blit(button_img,(550,280))
    #screen.blit(button_img,(550,340))
    #screen.blit(button_img,(550,400))
    #print(pygame.event.get().type)
        #print(present_state)
    #screen.fill((0,0,0))
quit()


