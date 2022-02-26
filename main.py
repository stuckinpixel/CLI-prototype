
import pygame, sys, time, random, json, math
from datetime import datetime
from pygame.locals import *

ROWS, COLS = 25, 60
UNIT_Y, UNIT_X = 20, 13
font_size = 15

pygame.init()
WIDTH, HEIGHT = COLS*UNIT_X, ROWS*UNIT_Y
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=64
ft=pygame.time.Clock()
pygame.display.set_caption('CLI Modal')

pygame.font.init()
font = pygame.font.SysFont('Verdana', font_size)

class Compiler:
    def __init__(self):
        self.commands = [
            ["help", "to know what are the commands we can use"],
            ["time", "to know time"],
            ["clear", "to clear the screen"]
        ]
    def preprocess(self, command):
        result = command.strip().split(" ",)
        while " " in result:
            result.remove(" ")
        while "" in result:
            result.remove("")
        return result
    def get_help_string(self):
        result = ["Please use the commands below", ""]
        for row in self.commands:
            result.append(row[0]+" - "+row[1])
        result.append("")
        return result[:]
    def compile(self, path, command):
        result = []
        query = self.preprocess(command)
        result = ["Good Morning"]
        if len(query)==2:
            if query[0]=="cd":
                if query[1]=="..":
                    path = path[:-1]
                else:
                    path.append(query[1])
                result = []
        elif len(query)==1:
            if query[0]=="help":
                result = self.get_help_string()
            elif query[0]=="time":
                now = datetime.now()
                result = [now.strftime("%m/%d/%Y, %H:%M:%S")]
            elif query[0]=="clear":
                result = "__CLEAR__"
        return path, result


class Interface:
    def __init__(self):
        self.data = []
        self.path = ["users", "Monday"]
        self.initialize_data()
        self.input = ""
        self.compiler = Compiler()
    def initialize_data(self):
        self.data = [
            self.get_main_strip()
        ]
    def get_main_strip(self):
        return ">>> "+"/".join(self.path)+" > "
    def clear(self):
        self.initialize_data()
    def enter(self):
        if len(self.input)==0:
            self.data.append(self.get_main_strip())
        else:
            self.path, answer = self.compiler.compile(self.path, self.input)
            if answer == "__CLEAR__":
                self.input = ""
                self.clear()
            else:
                self.data += answer
                self.data.append(self.get_main_strip())
                self.input = ""
        if len(self.data)>=ROWS:
            self.data.pop(0)
            self.data.append(self.get_main_strip())
    def add_input(self, character):
        self.input += character
        self.data[-1] += character
    def backspace(self):
        if len(self.input)>0:
            self.input = self.input[:-1]
            self.data[-1] = self.data[-1][:-1]


class App:
    def __init__(self, surface):
        self.surface = surface
        self.play = True
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": (5, 5, 5),
            "alpha": (20, 210, 30),
            "strip": (20, 30, 210)
        }
        self.interface = Interface()
    def write_font(self, character, x, y, color):
        textsurface = font.render(character, True, color)
        self.surface.blit(textsurface,(x, y))
    def draw_layout(self):
        for i in range(ROWS):
            y = i*UNIT_Y
            is_strip = False
            if i<=(len(self.interface.data)-1):
                if len(self.interface.data[i])>3:
                    if self.interface.data[i][0]==">" and self.interface.data[i][1]==">" and self.interface.data[i][2]==">":
                        is_strip = True
                if is_strip:
                    end_index = self.interface.data[i].index(" > ") + 3
                for j in range(COLS):
                    x = j*UNIT_X
                    pygame.draw.rect(self.surface, self.color["alpha"], (x, y, UNIT_X, UNIT_Y), 1)
                    color = self.color["alpha"]
                    if is_strip:
                        if j<end_index:
                            color = self.color["strip"]
                    if j<=(len(self.interface.data[i])-1):
                        pass
                        self.write_font(self.interface.data[i][j], x, y, color)
    def print_data(self):
        for row in self.interface.data:
            print (row)
            print (self.interface.input)
        print ()
    def render(self):
        self.draw_layout()
        # self.print_data()
    def run(self):
        while self.play:
            self.surface.fill(self.color["background"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        self.play=False
                    elif event.key==K_RETURN:
                        self.interface.enter()
                    elif event.key==K_BACKSPACE:
                        self.interface.backspace()
                    else:
                        try:
                            character = chr(event.key)
                            self.interface.add_input(character)
                        except:
                            print ("don't use that key")
            #--------------------------------------------------------------
            self.render()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)



if  __name__ == "__main__":
    app = App(surface)
    app.run()
