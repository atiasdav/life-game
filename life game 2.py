from tkinter import *
from tkinter import ttk
import numpy as np
from PIL import Image

class state:

    # 2-Dim Array
    def __init__(self):
        self.rows = 100
        self.cols = 100
        self.arr = np.zeros((100, 100), dtype=int)

    # fills array with a cool pattern
    def Initail_Example(self):
        self.arr = np.zeros((100, 100), dtype=int)
        self.arr[50][50] = 1
        self.arr[50][51] = 1
        self.arr[50][49] = 1
        self.arr[52][50] = 1
        self.arr[53][50] = 1
        self.arr[54][50] = 1
        #-----another example------
        # self.arr[50][50] = 1
        # self.arr[50][51] = 1
        # self.arr[51][51] = 1
        # self.arr[52][50] = 1
        # self.arr[52][49] = 1
        # self.arr[52][51] = 1

    # convert a binary array to a black and white image
    def ConvArrToPicArr(self):
        for row in range(self.rows):
            for index, number in enumerate(self.arr[row]):
                if number == 0:
                    self.arr[row][index] = 255

    # print a 2-Dim array (for text UI)
    def printstate(self):
        for row in range(self.rows):
            print(self.arr[row])
        print()

    # return the state of a single cell (dead =0 / alive = 1)
    def ifalive(self, loci, locj):
        NumOfNeighbours = 0

        # ---determine the search range of a cell in regards to the cell location
        if loci == 0:
            rangei = [0, 1]
        elif loci == self.rows - 1:
            rangei = [-1, 0]
        else:
            rangei = [-1, 0, 1]
        if locj == 0:
            rangej = [0, 1]
        elif locj == self.cols - 1:
            rangej = [-1, 0]
        else:
            rangej = [-1, 0, 1]

        # count the cell Neighbours
        for i in rangei:
            for j in rangej:
                if self.arr[loci + i][locj + j] == 1:
                    NumOfNeighbours += 1
        if (self.arr[loci][locj]):
            NumOfNeighbours -= 1

        # return the state of a cell by those rules
        if NumOfNeighbours < 2 or NumOfNeighbours > 3:  # Any live cell with fewer than two live neighbours dies, as if by underpopulation & Any live cell with more than three live neighbours dies, as if by overpopulation.
            return 0
        if NumOfNeighbours == 2:  # Any live cell with two live neighbours lives on to the next generation.
            return self.arr[loci][locj]
        if NumOfNeighbours == 3:  # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            return 1

    # save an image of the state
    def imagefy(self):
        scale=8
        self.ConvArrToPicArr()
        array = np.array(self.arr)  # convert 2-Dim list to a numpy array
        array = array.astype(np.uint8)
        data = Image.fromarray(array)  # convert an array to an image object
        (width, height) = (data.width * scale, data.height * scale)
        resized_image = data.resize((width, height), resample=Image.BOX)
        resized_image.save('currstate.png')


# return a state class object of the next step of the game
def nextstep(curr):
    temp = state()
    # for each cell in a state determines if its alive or dead and save the new state
    for i in range(curr.rows):
        for j in range(curr.cols):
            temp.arr[i][j] = curr.ifalive(i, j)
    return temp

# GUI of the game
class LifeApp:
    def __init__(self, master):
        # program
        self.discrete = 1  # 1 mean that normal mode. 0 mean continues (start) mode
        self.step_counter = 0
        self.speed = 500
        self.curr = state()  # a 100x100 array
        self.curr.Initail_Example()  # fills with example pattern
        self.next = nextstep(self.curr)
        self.curr.imagefy()

        # icon and title of main screen
        master.title('Life Game')
        IconTitle = PhotoImage(file='GUIicon.png')
        master.iconphoto(False, IconTitle)

        # nav frame
        frame1 = ttk.Frame(master)
        frame1.grid(row=0, column=0)
        frame1.config(padding=(30, 15), relief=FLAT)
        master.resizable(False, False)

        self.label = ttk.Label(frame1, text="David Atias’s Game of Life!")
        self.label.grid(row=0, column=0, columnspan=3)
        self.label.config(font=('Ariel', 18))

        self.NS = ttk.Button(frame1, text="Next Step", command=self.nextstep)
        self.NS.grid(row=1, column=0)
        self.start_button = ttk.Button(frame1, text="Start", command= lambda:[self.workaround(),self.start()])
        self.start_button.grid(row=1, column=1)
        self.stop_button = ttk.Button(frame1, text="stop", command=self.stop)
        self.resett = ttk.Button(frame1, text="reset", command=self.resett)
        self.resett.grid(row=1, column=2)

        # pic frame
        self.frame2 = ttk.Frame(master, height=500, width=500)
        self.frame2.grid(row=1, column=0, pady=10)
        self.img_of_curr_state = PhotoImage(file="currstate.png")
        self.actPhoto = ttk.Label(self.frame2, image=self.img_of_curr_state)
        self.actPhoto.grid(row=0, column=0)

        # step_counter label
        self.frame3 = ttk.Frame(master)
        self.frame3.grid(row=2, column=0, pady=10)
        self.labelC = ttk.Label(self.frame3, text=f"step_counter: {self.step_counter}")
        self.labelC.grid(row=0, column=0)
        self.labelC.config(font=('Ariel', 10))

        # speed label
        self.speed_label = ttk.Label(self.frame3, text=f"speed: {1000 / self.speed}")
        self.speed_label.config(font=('Ariel', 10))
        self.scale = ttk.Scale(self.frame3, orient=HORIZONTAL, length=300, variable=self.speed, from_=1000, to=10)
        self.scale.set(500)

        # --menu--
        master.option_add('*tearOff', False)
        menubar = Menu(master)
        master.config(menu=menubar)
        file = Menu(menubar)
        help_ = Menu(menubar)
        menubar.add_cascade(menu=file, label='File')
        file.add_command(label='Exit', command=master.quit)
        menubar.add_cascade(menu=help_, label='Help')
        help_.add_command(label='About', command=self.about)

    def nextstep(self):
        self.previous = self.curr
        self.curr = self.next
        self.next = nextstep(self.next)
        self.curr.imagefy()
        self.img_of_curr_state = PhotoImage(file="currstate.png")
        self.actPhoto.config(image=self.img_of_curr_state)
        self.step_counter += 1
        self.labelC.config(text=f"step_counter: {self.step_counter}")

    def workaround(self):
        self.discrete = 0

    def start(self):
        if not self.discrete:
            self.start_button.grid_forget()
            self.stop_button.grid(row=1, column=1)
            self.scale.grid(row=1, column=0, columnspan=3)
            self.speed = int(self.scale.get())
            self.speed_label.config(text=f"speed: {round(1000 / self.speed, 2)}")
            self.speed_label.grid(row=0, column=3, padx=40)
            self.nextstep()
            self.actPhoto.after(self.speed, self.start)

    def stop(self):
        self.discrete = 1
        self.stop_button.grid_forget()
        self.scale.grid_forget()
        self.start_button.grid(row=1, column=1)

    def resett(self):
        self.discrete = 1
        self.step_counter = 0
        self.labelC.config(text=f"step_counter: {self.step_counter}")
        self.speed_label.grid_forget()
        self.scale.grid_forget()
        self.stop_button.grid_forget()
        self.start_button.grid(row=1, column=1)
        self.curr.Initail_Example()
        self.next = nextstep(self.curr)
        self.curr.imagefy()
        self.img_of_curr_state = PhotoImage(file="Currstate.png")
        self.actPhoto.config(image=self.img_of_curr_state)

    def about(self):
        window = Toplevel()
        window.title('About')
        mell = ttk.Frame(window)
        mell.pack()
        mell.config(padding=(30, 15), relief=FLAT)
        self.label2 = ttk.Label(mell,
                                text='David Atias’s Game of Life! V2.0\nThis game was developed by David Atias.\nEmail: atiasdav@gmail.com \
                                     \n\nThe game rules are:\n1.Any live cell with fewer than two live neighbours dies, as if by underpopulation & Any live cell with more than three live neighbours dies, as if by overpopulation.\n2.Any live cell with two live neighbours lives on to the next generation.\n3.Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.')
        self.label2.grid(row=0, column=0, columnspan=1)
        self.label2.config(font=('Ariel', 11))
        # ttk.Label(mell,text="\n\nKnown issues:\n1.cant restart after stop.\n2.reset don't reset properly the after stop",font=('Ariel', 11)).grid(row=1, column=0, columnspan=1,sticky=SW) -> resolved

def main():
    root = Tk()
    LifeApp(root)
    root.mainloop()

if __name__ == "__main__": main()