import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
from PIL import Image
import webbrowser
import matplotlib


matplotlib.use("Agg")  # tells matplotlib to not create hidden root
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from urllib3.util import url
from data import *
from artist_links import *
from tkinter import messagebox


"""Window"""
def main():
   root = tk.Tk()
   root.resizable(width=False, height=False)
   root.title("SpottyFly")
   root.geometry("650x400")
   root.configure(bg="black")
   SpottyFlyApp(root)
   root.mainloop()




"""SpottyFly App"""
class SpottyFlyApp:
   def __init__(self, root):
       ctk.set_appearance_mode("dark")
       self.root = root
       self.canvas = None
       self.artist_links = artist_links
       self.current_genre_artists = [] #hold the list of genres/makes sure that genre pops up when typed
       self.in_genre_mode = True #tracks if user is in genre selection mode


       """logo"""
       logo = ctk.CTkImage(light_image=Image.open('Images/SpottyflyLogo.png'),
                           dark_image=Image.open('Images/SpottyflyLogo.png'), size=(90, 90))
       Llogo = ctk.CTkLabel(self.root, text='', image=logo)
       Llogo.place(x=60, y=18)


       """Placeholder Image"""
       CircleQ = ctk.CTkImage(light_image=Image.open('Images/MissingArtist.png'),
                              dark_image=Image.open('Images/MissingArtist.png'), size=(180, 180))
       LCircleQ = ctk.CTkLabel(self.root, text='', image=CircleQ)
       LCircleQ.place(x=417, y=125)


       """Data"""
       self.music_artists_by_genre = {
           "Pop": [
               "Taylor Swift",
               "Ariana Grande",
               "Dua Lipa",
               "Olivia Rodrigo",
               "Harry Styles"
           ],


           "Hip-Hop": [
               "Drake",
               "Travis Scott",
               "Lil Uzi Vert",
               "Kendrick Lamar"
           ],


           "Rock": [
               "Imagine Dragons",
               "Foo Fighters",
               "Arctic Monkeys",
               "Nirvana",
               "Green Day",
               "Harry Styles"
           ],


           "R&B": [
               "SZA",
               "The Weeknd",
               "Brent Faiyaz",
               "H.E.R.",
               "Daniel Caesar",
               "Ariana Grande",
               "Drake"
           ],


           "Rap": [
               "Nicki Minaj",
               "21 Savage",
               "Lil Baby",
               "J. Cole"
           ]
       }
       self.new_dict = {key.lower().strip(): value for key, value in self.music_artists_by_genre.items()}
       self.create_widgets()
       self.update(self.music_artists_by_genre)


   """Widgets"""
   def create_widgets(self):

       """Title"""
       self.title_label = ctk.CTkLabel(self.root, text="SPOTTYFLY", font=("Fixedsys", 60, "bold"), fg_color="black",
                                       text_color="#36C64E")
       self.title_label.place(x=165, y=25)


       """Search bar"""
       self.my_entry = ctk.CTkEntry(self.root, font=("Terminal", 12), placeholder_text='[Select a Genre]',
                                    fg_color="#2b2a2a", corner_radius=15,
                                    border_width=1, text_color="white", width=212, height=35, state='disabled')
       self.my_entry.place(x=25, y=120)
       self.my_entry.bind("<KeyRelease>", self.check)
       self.my_entry.bind("<Return>", lambda e: messagebox.showinfo("Hold on!", "Please click the Enter button on screen."))


       """1st Enter btn"""
       self.enter = ctk.CTkButton(self.root, text="Enter", font=("Terminal", 10, "bold"), corner_radius=10,
                                  border_width=1, border_color="grey", fg_color="black", text_color="white",
                                  width=60, height=35, command=self.enter_btn1)
       self.enter.place(x=241, y=120)


       """Artist names"""
       self.artistName = ctk.CTkLabel(self.root, text="Artist", font=("Fixedsys", 22, "bold", "underline"), fg_color="black",
                                      text_color="white")
       self.artistName.place(x=509, y=340, anchor="center")
       self.artistName.bind("<Button-1>", self.open_link)


       """Listbox containing the artists"""
       self.my_list = tk.Listbox(self.root, width=21, height=7, fg="white", bg='#111316', font=("Fixedsys", 17),
                                 bd=1, highlightbackground="#111316")
       self.my_list.place(x=25, y=165)
       self.my_list.bind("<<ListboxSelect>>", self.fillout)


       """Back buttons"""
       self.back_button = ctk.CTkButton(self.root, text="Back", font=("Terminal", 10, "bold"), corner_radius=10,
                                        border_width=1, border_color="grey", fg_color="black", text_color="white",
                                        width=60, height=35, command=self.back_btn)
       self.back_button.place_forget()


       """Pi chart button"""
       self.pibutton = ctk.CTkButton(self.root, text="Genre\nChart", font=("Terminal", 10, "bold"), corner_radius=10,
                                     border_width=1, border_color="grey", fg_color="black", text_color="white",
                                     width=60, height=35, command=self.show_genre_pie)
       self.pibutton.place(x=305, y=120)


   """Update the listbox list"""
   def update(self, data):
       self.my_list.delete(0, tk.END)
       for item in data:
           self.my_list.insert(tk.END, item)

   """Fill the entry box with data in list"""
   def fillout(self, event):
       sel = self.my_list.get(tk.ACTIVE)
       self.my_entry.configure(state="normal")
       self.my_entry.delete(0, tk.END)
       self.my_entry.insert(0, sel)
       self.my_entry.configure(state="disabled")

   """Fill/update the list based on entrybox"""
   def check(self, event):
       typed = self.my_entry.get()
       if typed is None:
           return
       typed = typed.lower().strip()
       if self.in_genre_mode:
           data = [genre for genre in self.music_artists_by_genre if typed in genre.lower()]
       else:
           data = [artist for artist in self.current_genre_artists if typed in artist.lower()]
       self.update(data)


   """Makes pi chart for genres"""
   def show_genre_pie(self):
       labels = []
       sizes = []
       for genre, artists in self.music_artists_by_genre.items():
           labels.append(genre)
           sizes.append(len(artists))

       theme_colors = ['#006400', '#228B22', '#2E8B57', '#3CB371', '#66CDAA', '#8FBC8F', '#98FB98', '#90EE90']

       """create window"""
       win = tk.Toplevel(self.root)
       win.title("Genre Pie chart")

       """draw the pie in the window"""
       fig = plt.Figure(figsize=(4, 4), facecolor='black')
       ax = fig.add_subplot(111, facecolor='black')
       ax.set_title('Spottyfly Genre Pie Chart', color='white', fontweight='bold', fontsize=17, pad=15)
       ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=theme_colors, textprops={'color': 'white'})
       ax.axis('equal')
       canvas = FigureCanvasTkAgg(fig, master=win)
       canvas.get_tk_widget().pack(fill='both', expand=True)
       canvas.draw()


   """Artist links function"""
   def open_link(self, event):
       artist = self.artistName.cget("text")#Gets the name of the artist shown on "artistName"
       url = self.artist_links.get(artist)#matches it with list of artists found in "artists_links.py" using artist name
       if url:
           webbrowser.open(url) #if url found, opens link


   """Enter btn1 function"""
   def enter_btn1(self, event=None):
       ent = self.my_entry.get().lower().strip()
       if ent in self.new_dict:
           self.my_entry.configure(placeholder_text='[Select an Artist]')

           results = self.new_dict[ent]
           self.update(results)

           self.create_artist_button() #shows the artists of selected genre
           self.in_genre_mode = False #Switches it to artist selections
           self.current_genre_artists = results
           self.current_genre_artists = self.new_dict[ent]
           self.back_button.place(x=241, y=120)


   """2nd Enter button for artist selection"""
   def create_artist_button(self):
       self.enter2 = ctk.CTkButton(self.root, text="Enter", font=("Terminal", 10, "bold"), corner_radius=10,
                                   border_width=1, border_color="grey", fg_color="black", text_color="white",
                                   width=60, height=35, command=self.enter_btn2)
       self.enter2.place(x=304, y=120)




   """Enterbtn2 functionality"""
   def enter_btn2(self, event=None):
       ent = self.my_entry.get().lower().strip()
       artist_name = self.my_list.get(tk.ACTIVE)
       self.artistName.configure(text=artist_name)#shows artistName label when pressed


       """show graph and the images based on the name of artist"""
       if artist_name.lower() == "taylor swift":
           Taylor = ctk.CTkImage(light_image=Image.open('Images/TaylorSwift.png'),
                                 dark_image=Image.open('Images/TaylorSwift.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=Taylor)
           Artist_Image.place(x=417, y=125)
           self.graph("taylor swift")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "ariana grande":
           AR = ctk.CTkImage(light_image=Image.open('Images/ArianaGrande.png'),
                             dark_image=Image.open('Images/ArianaGrande.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=AR)
           Artist_Image.place(x=417, y=125)
           self.graph("ariana grande")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "dua lipa":
           DuaL = ctk.CTkImage(light_image=Image.open('Images/DuaLipa.png'),
                               dark_image=Image.open('Images/DuaLipa.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=DuaL)
           Artist_Image.place(x=417, y=125)
           self.graph("dua lipa")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "olivia rodrigo":
           OR = ctk.CTkImage(light_image=Image.open('Images/OliviaRodrigo.png'),
                             dark_image=Image.open('Images/OliviaRodrigo.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=OR)
           Artist_Image.place(x=417, y=125)
           self.graph("olivia rodrigo")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "harry styles":
           HS = ctk.CTkImage(light_image=Image.open('Images/HarryStyles.png'),
                             dark_image=Image.open('Images/HarryStyles.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=HS)
           Artist_Image.place(x=417, y=125)
           self.graph("harry styles")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "drake":
           Dke = ctk.CTkImage(light_image=Image.open('Images/Drake.png'), dark_image=Image.open('Images/Drake.png'),
                              size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=Dke)
           Artist_Image.place(x=417, y=125)
           self.graph("drake")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "travis scott":
           TS = ctk.CTkImage(light_image=Image.open('Images/TravisScott.png'),
                             dark_image=Image.open('Images/TravisScott.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=TS)
           Artist_Image.place(x=417, y=125)
           self.graph("travis scott")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "lil uzi vert":
           LUV = ctk.CTkImage(light_image=Image.open('Images/LilUzi.png'), dark_image=Image.open('Images/LilUzi.png'),
                              size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=LUV)
           Artist_Image.place(x=417, y=125)
           self.graph("lil uzi vert")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "kendrick lamar":
           KL = ctk.CTkImage(light_image=Image.open('Images/Kendrick.png'),
                             dark_image=Image.open('Images/Kendrick.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=KL)
           Artist_Image.place(x=417, y=125)
           self.graph("kendrick lamar")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "j. cole":
           JC = ctk.CTkImage(light_image=Image.open('Images/Cole.png'), dark_image=Image.open('Images/Cole.png'),
                             size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=JC)
           Artist_Image.place(x=417, y=125)
           self.graph("j. cole")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "imagine dragons":
           ID = ctk.CTkImage(light_image=Image.open('Images/ImagineDragons.png'),
                             dark_image=Image.open('Images/ImagineDragons.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=ID)
           Artist_Image.place(x=417, y=125)
           self.graph("imagine dragons")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "foo fighters":
           FF = ctk.CTkImage(light_image=Image.open('Images/FooFighters.png'),
                             dark_image=Image.open('Images/FooFighters.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=FF)
           Artist_Image.place(x=417, y=125)
           self.graph("foo fighters")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "arctic monkeys":
           AM = ctk.CTkImage(light_image=Image.open('Images/ArcticMonkeys.png'),
                             dark_image=Image.open('Images/ArcticMonkeys.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=AM)
           Artist_Image.place(x=417, y=125)
           self.graph("arctic monkeys")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "nirvana":
           NVA = ctk.CTkImage(light_image=Image.open('Images/Nirvana.png'),
                              dark_image=Image.open('Images/Nirvana.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=NVA)
           Artist_Image.place(x=417, y=125)
           self.graph("nirvana")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "green day":
           GD = ctk.CTkImage(light_image=Image.open('Images/GreenDay.png'),
                             dark_image=Image.open('Images/GreenDay.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=GD)
           Artist_Image.place(x=417, y=125)
           self.graph("green day")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "sza":
           SZA = ctk.CTkImage(light_image=Image.open('Images/SZA.png'), dark_image=Image.open('Images/SZA.png'),
                              size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=SZA)
           Artist_Image.place(x=417, y=125)
           self.graph("sza")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "the weeknd":
           TWD = ctk.CTkImage(light_image=Image.open('Images/TheWeeknd.png'),
                              dark_image=Image.open('Images/TheWeeknd.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=TWD)
           Artist_Image.place(x=417, y=125)
           self.graph("the weeknd")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "brent faiyaz":
           BF = ctk.CTkImage(light_image=Image.open('Images/BrentFaiyaz.png'),
                             dark_image=Image.open('Images/BrentFaiyaz.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=BF)
           Artist_Image.place(x=417, y=125)
           self.graph("brent faiyaz")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "h.e.r.":
           HER = ctk.CTkImage(light_image=Image.open('Images/HER.png'), dark_image=Image.open('Images/HER.png'),
                              size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=HER)
           Artist_Image.place(x=417, y=125)
           self.graph("h.e.r.")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "daniel caesar":
           DC = ctk.CTkImage(light_image=Image.open('Images/DanielCaesar.png'),
                             dark_image=Image.open('Images/DanielCaesar.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=DC)
           Artist_Image.place(x=417, y=125)
           self.graph("daniel caesar")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "nicki minaj":
           NM = ctk.CTkImage(light_image=Image.open('Images/NickiMinaj.png'),
                             dark_image=Image.open('Images/NickiMinaj.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=NM)
           Artist_Image.place(x=417, y=125)
           self.graph("nicki minaj")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "21 savage":
           SAV = ctk.CTkImage(light_image=Image.open('Images/21Savage.png'),
                              dark_image=Image.open('Images/21Savage.png'), size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=SAV)
           Artist_Image.place(x=417, y=125)
           self.graph("21 savage")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)
       elif artist_name.lower() == "lil baby":
           LB = ctk.CTkImage(light_image=Image.open('Images/LilBaby.png'), dark_image=Image.open('Images/LilBaby.png'),
                             size=(180, 180))
           Artist_Image = ctk.CTkLabel(self.root, text='', image=LB)
           Artist_Image.place(x=417, y=125)
           self.graph("lil baby")
           self.clicky = ctk.CTkLabel(self.root, text="^^^Click For Youtube^^^", text_color="white", font=("Terminal", 8))
           self.clicky.place(x=445, y=365)

       self.back_button.place(x=241, y=120) #Shows the second back button


   """Back button functionality"""
   def back_btn(self):
       self.my_list.delete(0, tk.END)
       self.update(self.music_artists_by_genre)# Reset Listbox
       self.my_entry.delete(0, 'end')# Clears search bar
       self.artistName.configure(text="Artist")# Reset the artist name label
       self.back_button.place_forget()# Hide the back button
       self.in_genre_mode = False #Switches it back to genre mode/ genre selection
       self.current_genre_artists = []#Resets the artist list
       self.enter2.place_forget()# Hides the 2nd enter button for artist selection
       self.my_entry.configure(placeholder_text='[Select a Genre]')# Reset the placeholder text for genre search
       self.clicky.destroy()# Removes the "Click for Youtube" label

       """Remove the graph"""
       if hasattr(self, 'Artist_Image'):
           self.Artist_Image.destroy()

       """Adds back the placeholder circle"""
       CircleQ = ctk.CTkImage(light_image=Image.open('Images/MissingArtist.png'), dark_image = Image.open('Images/MissingArtist.png'), size=(180, 180))
       LCircleQ = ctk.CTkLabel(self.root, text = '', image=CircleQ)
       LCircleQ.place(x=417, y=125)

       """Remove the graph (if it exists)"""
       if hasattr(self, 'canvas') and self.canvas:
           self.canvas.get_tk_widget().destroy()
           self.canvas = None


   """replaces the "artist_name" based on the data file"""
   def graph(self, artist_name):
       artist_data = {
           #POP
           "taylor swift": taylor_data,
           "ariana grande": ariana_data,
           "dua lipa": dua_data,
           "olivia rodrigo": olivia_data,
           "harry styles": harry_data,
           #HIP-HOP
           "drake": drake_data,
           "travis scott": travis_data,
           "lil uzi vert": uzi_data,
           "kendrick lamar": kendrick_data,
           "j. cole": cole_data,
           #ROCK
           "imagine dragons": imagine_data,
           "foo fighters": foo_data,
           "arctic monkeys": arctic_data,
           "nirvana": nirvana_data,
           "green day": green_data,
           #RNB
           "sza": sza_data,
           "the weeknd": weeknd_data,
           "brent faiyaz": brent_data,
           "h.e.r.": her_data,
           "daniel caesar": daniel_data,
           #RAP
           "nicki minaj": nicki_data,
           "21 savage": twenty_one_data,
           "lil baby": lil_baby_data
       }

       data = artist_data.get(artist_name.lower())


       """Setting up graph + customizations"""
       if self.canvas is None:
        if data:
            width = self.root.winfo_width()
            height = self.root.winfo_height()

            fig, ax = plt.subplots(figsize=(width / 190, height / 180), facecolor='#111316')  # Set background color
            ax.bar(data.keys(), data.values(), color="#36C64E")
            ax.set_title(f"{artist_name.title()}'s Listeners, 2020–2025", color="white")
            ax.set_xlabel("Year", color="white")
            ax.set_ylabel("Listeners (Millions)", color="white")
            ax.set_facecolor('#111316')#Back of bg color

        """Changes the spine/edge color"""
        for spine in ax.spines.values():
            spine.set_edgecolor('black')#corner and edge lines of the box color


        ax.tick_params(axis='x', colors='white', length=0)
        ax.tick_params(axis='y', colors='white', length=0) #Remove the dashes near the numbers


        plt.tight_layout() #Fits the graph


        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=25, y=163)


"""runs program"""
if __name__ == "__main__":
   main()