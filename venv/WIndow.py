from tkinter import *
import main
root = Tk()

window = Toplevel(root)
root.attributes("-alpha",0.0)
def onRootIconify(event): window.withdraw()
root.bind("<Unmap>", onRootIconify)
def onRootDeiconify(event): window.deiconify()
root.bind("<Map>", onRootDeiconify)



def get_pos(event):
    xwin = window.winfo_x()
    ywin = window.winfo_y()
    startx = event.x_root
    starty = event.y_root

    ywin = ywin - starty
    xwin = xwin - startx

    def move_window(event):
        window.geometry("440x320" + '+{0}+{1}'.format(event.x_root + xwin, event.y_root + ywin))

    startx = event.x_root
    starty = event.y_root

    title_bar.bind('<B1-Motion>', move_window)




window.overrideredirect(True)
w = 440
h = 320
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.config(background="#1A1A1A")

title_bar = Frame(window, bg='#2ECC71', relief='raised', bd=2)
close_button = Button(title_bar, text='X', command=root.destroy)

title_bar.pack(fill=X)
close_button.pack(side=RIGHT)
title_bar.bind('<B1-Motion>', get_pos)


class StateManager():
    def __init__(self):
        self.start = StartState()
        self.menu = None
        self.current_state = self.start

    def next_state(self, function, exists = False):
        if exists:
            self.current_state.close()
            self.current_state = function
            self.current_state.open()
        else:
            current_state = function()
            if current_state != None:
                print(self.menu)
                print(self.current_state)
                self.current_state = current_state
                print(self.current_state)
                self.current_state.open()

    def openStart(self):
        self.current_state.open()

    def change(self, state):
        print(state,1)
        self.menu = state


class StartState(StateManager):
    def __init__(self):
        self.frame = Frame(window, background="#1A1A1A")
        frame = self.frame
        self.word = Label(frame, text="spotify v2.0", background="#1A1A1A",
                          fg="#2ECC71", font=("Gotham Black", 40), padx= 20, pady= 20)
        self.word2 = Label(frame, text="Enter Your Name", background="#1A1A1A",
                           fg="white", font=("Roboto Thin", 15))
        self.textbox = Entry(frame, text = "Enter Your Name")
        self.button = Button(frame, text="Swag Like Ohio", command = lambda: start.next_state(self.close), background="#2ECC71")

    def close(self, placeholder = None):
        if self.textbox.get() != "":
            self.frame.pack_forget()
            self.textbox.unbind('<Return>')
            menu = MenuState(self.textbox.get(), 10, 1)
            (lambda: start.change(menu))()
            return menu
        else:
            self.word2.configure(text="Invalid Name")

    def open(self):
        self.frame.pack()
        self.word.pack()
        self.word2.pack(padx=5)
        self.textbox.pack(pady=20, padx=20)
        self.textbox.bind('<Return>', lambda x : start.next_state(self.close))
        self.button.pack()

class MenuState():
    def __init__(self, name, songs, week):
        self.name = name
        self.songs = songs
        self.week_num = week
        self.user = main.User(name)
        self.frame = Frame(window, background="#1A1A1A")
        self.week = Label(window, text=f"Week\n {self.week_num}", background="#2ECC71",
                          fg="white", font=("Gotham Black", 20))

        frame = self.frame
        self.name = Label(frame, text=f"Name: {self.name}", background="#1A1A1A",
                          fg="white", font=("Roboto Thin", 20))
        self.songs = Label(frame, text=f"Songs: {len(self.user.listened_songs)}", background="#1A1A1A",
                          fg="white", font=("Roboto Thin", 20))
        self.discover_weekly = Button(frame, text="Discover Weekly", command = lambda: start.next_state(self.discover_week))
        self.playlists = Button(frame, text="Playlist", command = self.close)


    def close(self, placeholder = None):
        self.frame.pack_forget()

    def open(self):
        self.week.configure(text=f"Week\n{self.week_num}")
        self.songs.configure(text=f"Songs: {len(self.user.listened_songs)}")
        self.frame.place(x= 230, y=80)
        self.week.place(bordermode=OUTSIDE, height=170, width=170, x= 20, y=80)
        self.name.pack(anchor=W)
        self.songs.pack(anchor=W)
        self.discover_weekly.pack(padx=10, pady=10)
        self.playlists.pack(padx=10, pady=10)


    def discover_week(self):
        start = DiscoverState(self.week_num, self.user)
        self.close()
        return start

    def next_week(self):
        self.week_num += 1


#test

class DiscoverState():
    def __init__(self, week, user):
        self.frame = Frame(window, background="#F5B041", bd=2)
        self.week = week
        self.user = user
        frame = self.frame
        self.songs_num = 10
        self.songs = Label(frame, text= self.get_songs(), background="#1A1A1A",
                          fg="white", font=("Gotham Black", 12),justify="left", wraplength=400)
        self.back = Button(frame, text="back", command = lambda: start.next_state(start.menu, True))

    def get_songs(self):
        result = ""
        week = self.week
        user = self.user
        if week == 1:
            discover_playlist = main.discover_week_1(user)
            result += f"Based on you're listening history we recommend these!\n \n"
        elif week == 2:
            discover_playlist = main.discover_week_2(user)
            result += f"You've recently been listening alot of {discover_playlist[1]}! \n \n"
        elif week == 3:
            discover_playlist = main.discover_week_3(user)
            result += f"You're {discover_playlist[1]} energy have been showing alot recently! \n \n"
        print(discover_playlist)
        for i, n in enumerate(discover_playlist[0]):
            result += f"{i + 1}) {n['title']} \n"

        user.change_playlist(discover_playlist[0], week)
        (lambda: start.menu.next_week())()
        return result

    def close(self, placeholder = None):
        self.frame.pack_forget()
    def open(self):
        self.frame.pack(fill=Y, expand= TRUE)
        self.songs.pack(fill= Y, expand= TRUE)
        self.back.pack()




start = StateManager()
start.openStart()

top = Frame(master=window)

top.mainloop()