from tkinter import *
from tkinter import ttk  # for Treeview
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence # to manipulate images
import os
import csv
import pandas as pd
from functools import lru_cache

# line 921, 966, unmodified lines

class EVcars():
    
    def __init__(self):
        
        self.window = Tk() 
        # Set high DPI awareness
        self.window.tk.call('tk', 'scaling', 1.25)
        # print(os.path.abspath("."))
        # print(os.getcwd())
        # print(self._get_filepath("win_logo.png"))

        icon = ImageTk.PhotoImage(Image.open(self._get_filepath("win_logo.png")))

        self.window.title("Ninjas EV Info Management System")
        self.window.iconphoto(True, icon) #set True to set that icon in all self.window & its descendents ,and to be changeabl later
        self.window.geometry("800x600")
        self.window.config(bg="lightgrey")

        # 15/12/24
        self.cur_dir = os.getcwd().split("\\")[-1]

        self.file = None 
        self.ori_data = None
        self.admin_pass = "12345"

        self.hist_dict = {} # to store what we type in entry as list # modified place
        self.val_lst = [] # I moved it here
        
        self.style = ttk.Style()

        self.home()
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

    def data_upload(self, data_path): # <===
        with open(data_path, newline="") as f:
            csv_reader = csv.reader(f)
            data =  [row for row in csv_reader]
            return data

    ## ==> HOME page
    def home(self):
        
        # self.window.state("normal")
        # self.window.resizable(False, False)
        self.isAdmin = False

        self.show_frame = Frame(self.window)
        self.show_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.show_frame.columnconfigure(0, weight=1)
        self.show_frame.rowconfigure(0, weight=1)


        a_img = Image.open(self._get_filepath("evcar.gif"))
        frames = ImageSequence.Iterator(a_img)
        img_label = Label(self.show_frame)
        self.window.after(115, lambda: self.animate_home(img_label, frames, a_img))
        img_label.place(x=0, y=0, relheight=1, relwidth=1)

        Label(self.show_frame, text="Welcome", font=("Helvectica", 35), borderwidth=0, bg="#D9F8FC")\
        .grid(row=0, column=0, sticky=N)

        log_in_frame = Frame(self.show_frame, bg="grey")
        log_in_frame.grid(row=0, column=0, sticky="n",pady=100)
        Label(log_in_frame, text="Log In", fg="white", bg="grey", font=("Helvectica", 15))\
            .grid(row=0, column=0)
        
        Label(log_in_frame, text="Username", fg="white", bg="grey")
        opt_lst = ["User", "Admin"]
        self.style.theme_use("vista")
        self.combobox = ttk.Combobox(log_in_frame, values=opt_lst, state="readonly", width=15, height=10, font=("Helvectica", 10, "bold"))
        self.combobox.grid(row=1, column=0, padx=20, ipady=5, pady=5)
        # self.combobox.configure(style="TCombobox")

        self.pass_lab = Label(log_in_frame, text="Password", fg="white", bg="grey")
        self.pass_ent = Entry(log_in_frame, show="*", width=17, font=("Helvectica", 10, "bold"))
        self.pass_ent.bind("<Return>", lambda event: self.check_pass())

        self.error_msg = Label(log_in_frame, text="", bg="grey")
        self.error_msg.grid(row=4, column=0)
        self.combobox.bind("<<ComboboxSelected>>", self.get_name)
        self.ok = Button(log_in_frame, text="Login", width=6, font="bold", state="disabled", activebackground="grey", command=self.check_pass)
        self.ok.grid(row=5, column=0, pady=10)

        prev_msg = ""
        msgs = iter(["Team-3\n", "SSM-15089(leader)", "SSM-15431", "SSM-15432", "SSM-5117"])
        lab = Label(self.show_frame, text="", compound="top", font=("", 13, "bold"), borderwidth=0, bg='#D6FCEE')
        lab.grid(row=0, column=0, sticky=W)
        lab2 = Label(self.show_frame, text="", font=("Helvectica", 20), bg="#727F8A")
        lab2.grid(row=1, column=0, sticky="ws")

        self.show_gp = self.window.after(2500, lambda: self.show_about(lab, lab2, prev_msg, msgs))

        self.quit_ico = PhotoImage(file=self._get_filepath("door.png"))
        quit_btn = Button(self.show_frame, text=" Quit", image=self.quit_ico, compound="left", width=65, height=25, activebackground="lightgrey", activeforeground="red", font=('Consolas', 11, 'bold'), command=self.window.destroy, cursor="hand2")
        quit_btn.grid(row=1, column=0, sticky=SE)
        
    def get_name(self, event):
        selected_val = self.combobox.get()
        self.combobox.set(selected_val)
        self.state = selected_val
        self.ok.config(state="normal")
        print(self.state)
        if selected_val == "Admin":
            self.pass_lab.grid(row=2, column=0)
            self.pass_ent.grid(row=3, column=0, ipady=5)
            self.pass_ent.focus_set()
        else:
            self.pass_lab.grid_forget() 
            self.pass_ent.grid_forget()
            self.combobox.bind("<Return>", lambda event: self.check_pass())
            self.error_msg.config(text="", fg="black")

    def check_pass(self):
        if self.state in ["User", "Admin"]:
            if self.state == "Admin":
                psw = self.pass_ent.get()
                if psw == self.admin_pass:
                    self.isAdmin = True
                    try:
                        self.createWidgets()
                        self.start_page()
                        self.window.resizable(True, True)
                    except Exception as e:
                        print(e)
                else:
                    self.error_msg.config(text="Incorrect password!", fg="red")
            else:
                self.isAdmin = False
                try:
                    self.createWidgets()
                    self.start_page()
                    self.window.resizable(True, True)
                except Exception as e:
                    print(e)

                
            
    def show_about(self, labl, labl2, prev_msg, msgs):
        self.gp_logo = ImageTk.PhotoImage(Image.open(self._get_filepath("group_logo.png")))
        try:
            msg = next(msgs)
            cur_msg = prev_msg + msg + "\n"
            try:
                labl.config(text=cur_msg, image=self.gp_logo, anchor="w")
                self.window.after(2500, lambda: self.show_about(labl, labl2, cur_msg, msgs))
            except TclError:
                pass
        except StopIteration:
            try:
                labl.grid_forget()
                prev_msg = "Presented By Team-3(The Python Ninjas)"
                labl2.config(text=prev_msg)
            except TclError:
                pass

    def animate_home(self, lab, frames, a_img):
        try :
            next(frames) # to skip very first frame
            frame = next(frames)
            img = ImageTk.PhotoImage(frame)
            self.a_img = img
            # used try except to by pass TclError 
            try:
                lab.config(image=img)
                self.window.after(115, lambda :self.animate_home(lab, frames, a_img)) # for whale - 50, for evcar -100
            except TclError:
                pass      
        except StopIteration:
            frames = ImageSequence.Iterator(a_img)
            self.window.after(115, lambda :self.animate_home(lab, frames, a_img))

    
    ## ===> Main page
    def createWidgets(self):
        top = self.window.winfo_toplevel()
        self.menuBar = Menu(top)
        top.config(menu=self.menuBar)
        self.subMenu = Menu(self.menuBar, tearoff=0)
        
        if self.isAdmin:
            self.menuBar.add_cascade(label="mode- Admin", state="disabled")
            self.window.bind("<Button-2>", self.chg_option)
        else:
            self.menuBar.add_cascade(label= "mode- User", state="disabled")

        self.menuBar.add_cascade(label=" Home ", command=lambda: [self.start_frame.tkraise(), self.dis_menu(" Home ")])
        self.menuBar.add_cascade(label=" Info ", activebackground="blue", command=self.show_cars_info_ico) 

    # def chg_back(self):
    #     # set it here again cuz I changed logo and title in on func
    #     try:
    #         self.window.iconphoto(True, PhotoImage(file="./Project/frame_logo/win_logo.png"))
    #         self.window.title("Ninjas EV Info Management System") 
    #     except:
    #         pass

    def dis_menu(self, name): #disable that name and set others normal
        try:
            menu = [" Home ", " Info "]
            for m in menu:
                if m == name:
                    self.menuBar.entryconfig(m, state='disabled')
                else:
                    self.menuBar.entryconfig(m, state=NORMAL)
        except:
            pass

    def clear_data(self):
        self.file = None 
        self.ori_data = None
        self.datas = None 

    def ask_confirm(self):
        response = messagebox.askokcancel("Confirmation", "Are you sure to log out?")
        if response:
            self.log_out()
        else:
            pass

    def load_file(self):

        file = filedialog.askopenfilename(
        initialdir=os.path.abspath("."),  #"C:/Users/Desktop/", #../MainFrame/Desk...
        initialfile="evcars_subset", 
        title="Open file", 
        filetypes=[("CSV file", "*.csv"),]#, ("Text file", "*.txt"), ("All file", "*")]
        )
        if file != "":
            self.file = file
        else:
            self.file

        if self.file:
            self.info_labl.config(image="", text="", bg="#838B8B")
            self.noti_labl.config(image=self.noti_box, text=f"{self.file.split('/')[-1]} is loaded.", compound="left")
            self.load_btn.config(image=self.load_ico, text=" Load Another File", width=170)

            with open(self.file, newline='') as file:
                csv_reader = csv.reader(file) # one csvreader can be read only one time
                self.datas = [row for row in csv_reader]

            with open(self.file, newline='') as file:
                csv_reader = csv.reader(file)
                self.ori_data =  [row for row in csv_reader] # to use to reset data

            self.sorted_data = sorted(self.datas[1:], key=lambda a: (a[0], a[1])) # sorted data

    # animate using gif
    def gif_animation(self, btn, icon, a_icon):
        img_frames= ImageSequence.Iterator(a_icon)
        btn.bind("<Enter>", lambda event: self.hover_on(btn, img_frames, icon, a_icon, event))
        btn.bind("<Leave>", lambda event: self.hover_off(btn, icon, event))

    def hover_on(self, btn, img_frames, icon, a_icon, event):
        self.gif = self.window.after(15, lambda: self.animate_gif(btn, img_frames, icon, a_icon))
    
    def animate_gif(self, btn, img_frames, icon, a_icon):
        try:
            # for frame in frames:
            frame = next(img_frames)
            img = ImageTk.PhotoImage(frame)
            self.img = img # ***
            btn.config(image=self.img)
            self.gif = self.window.after(15, lambda: self.animate_gif(btn, img_frames, icon, a_icon))

        except StopIteration:
            img_frames = ImageSequence.Iterator(a_icon)
            self.gif = self.window.after(15, lambda: self.animate_gif(btn, img_frames, icon, a_icon))  # to continuously animate (reset the frames)

    
    def hover_off(self, btn, icon, event):
        
        self.window.after_cancel(self.gif)
        btn.config(image=icon)
    
    def log_out(self):

        self.home()
        try:
            self.brands_main_frame.destroy()
        except:
            print("There is no remaining file to destroy!")
        
        self.start_frame.destroy()
        self.menuBar.destroy()
        self.clear_data()
        
    # Second page
    def start_page(self):

        self.menuBar.entryconfig(" Home ", state='disabled')
        self.start_frame = Frame(self.window, bg="#838B8B")
        self.start_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame.destroy()
        
        if not self.isAdmin:  ##  <=====
            self.file = self._get_filepath("evcars_subset.csv")
            self.datas = self.data_upload(self.file)
            # for more csv file
            # data1= self.data_upload("")
            # data2= self.data_upload("")
            self.datas
            self.sorted_data = sorted(self.datas[1:], key=lambda a: (a[0], a[1]))
        else:
            self.file = None 
            self.datas = None

        self.style.theme_use('default')
        self.style.configure('Treeview.Heading', background="skyblue", font=("Consolas", 11, "bold"), rowheight=35)
        self.style.configure('Treeview', font=("Concolas", 9, "bold"), rowheight=25)

        self.start_frame.columnconfigure(0, weight=1)
        self.start_frame.rowconfigure(6, weight=1)

        # self.home_img = ImageTk.PhotoImage(Image.open("./Project/frame_logo/home_screen.png"))
        # Label(self.start_frame, image=self.home_img).place(x=0, y=0)

        self.load_a_ico = Image.open(self._get_filepath("data1.gif")) # to use in hover event
        self.load_ico = ImageTk.PhotoImage(Image.open(self._get_filepath("data1.gif")))

        self.noti_box = ImageTk.PhotoImage(Image.open(self._get_filepath("checked.png"))) # <==
        self.checked_ico = ImageTk.PhotoImage(Image.open(self._get_filepath("checked.png")))

        options_a_ico = Image.open(self._get_filepath("more.gif")) # icon must be image object before animating
        options_ico = ImageTk.PhotoImage(Image.open(self._get_filepath("more.gif")))
        
        shows_a_ico = Image.open(self._get_filepath("folder.gif"))
        shows_info_ico = ImageTk.PhotoImage(Image.open(self._get_filepath("folder.gif")))

        self.noti_labl = Label(self.start_frame, text="Please load file first!", bg="#838B8B", fg="white",  font=('Halvectica', 14, 'bold'))
        self.noti_labl.grid(row=0, column=0, columnspan=2, pady=10, ipadx=5, ipady=5)

        self.load_btn = Button(self.start_frame, text=" Load file",image=self.load_ico, compound="left", relief="raised", width=125, height=25, activebackground="lightblue", bg="lightblue", fg="black", font=('Consolas', 11, 'bold'), command=self.load_file, cursor="hand2")
        self.load_btn.grid(row=1, column=0, pady=5, ipadx=5, ipady=5)

        shows_info_btn = Button(self.start_frame, text=" Show Cars Info", activebackground="lightblue",image=shows_info_ico, compound="left", width=139, height=25, command=self.show_Info, bg="lightblue", fg="black", font=('Consolas', 11, 'bold'), cursor="hand2")
        shows_info_btn.grid(row=2, column=0, pady=20, ipadx=5, ipady=5)
        
        img= Image.open(self._get_filepath("convertible-car.gif"))#.resize((100, 100))
        car_labl = Label(self.start_frame, borderwidth=0, bg="#838B8B")        

        if not self.isAdmin: # <===
            self.noti_labl.config(image=self.noti_box, text=f"{self.file.split('/')[-1][:-4]}", compound="left")
            self.noti_labl.grid(row=0, column=0, columnspan=2, pady=10, ipadx=5, ipady=5)
            self.load_btn.grid_forget()
            car_labl.place(x=260, y=100, anchor="center")
        else:
            self.noti_labl.grid(row=0, column=0, columnspan=2, pady=10, ipadx=5, ipady=5)
            car_labl.place(x=260, y=167, anchor="center")

        frames = ImageSequence.Iterator(img)
        self.window.after(1000, lambda: self.animate_car(car_labl, frames, img))


        more_btn = Button(self.start_frame, activebackground="lightblue", text=" More", image=options_ico, compound="left", bg="lightblue", width=100, height=25, command=self.explore_Info, fg="black", font=('Consolas', 11, 'bold'), cursor="hand2")
        more_btn.grid(row=3, column=0, pady=20, ipadx=5, ipady=5)

        self.warn_box = ImageTk.PhotoImage(Image.open(self._get_filepath("error.png")))
        self.info_labl = Label(self.start_frame, text='', fg="red", bg="#838B8B", font=('Consolas', 11))
        self.info_labl.grid(row=4, column=0, sticky=S)  # Adjust row as needed

        logout_a_ico = Image.open(self._get_filepath("log-out.gif"))
        logout_ico = PhotoImage(file=self._get_filepath("door.png"))
        logout_btn = Button(self.start_frame, text=" Log Out", image=logout_ico, compound="left", width=100, height=30, activebackground="lightblue", bg="lightblue", activeforeground="red", font=('Consolas', 11, 'bold'), command= self.ask_confirm, cursor="hand2")
        logout_btn.grid(row=5, column=0, pady=10)

        # self.gp_name_box = ImageTk.PhotoImage(Image.open("./Project/frame_logo/gp_name_box.png").resize((570, 75)))
        # Label(self.start_frame, text="Presented by Team-3 (The Python Ninjas)", image=self.gp_name_box, compound="center", font=('Helvectica', 12, "bold"), bg="#838B8B").grid(row=6, column=0, sticky='ws')
    
        self.save_a_ico = Image.open(self._get_filepath("save-file.gif"))
        self.cancel_a_ico = Image.open(self._get_filepath("turn-left.gif"))
        self.confirm_a_ico = Image.open(self._get_filepath("yes-or-no.gif"))

        self.back_ico = ImageTk.PhotoImage(Image.open(self._get_filepath("back_ico.png")))
        self.save_ico = ImageTk.PhotoImage(Image.open(self._get_filepath("save.png")))
        self.cancel_ico = ImageTk.PhotoImage(Image.open(self._get_filepath("undo.png")))
        self.confirm_ico = ImageTk.PhotoImage(Image.open(self._get_filepath("confirm.png"))) 

        self.gif_animation(self.load_btn, self.load_ico, self.load_a_ico) # fumction to add gif animation
        self.gif_animation(logout_btn, logout_ico, logout_a_ico)
        self.gif_animation(more_btn, options_ico, options_a_ico)
        self.gif_animation(shows_info_btn, shows_info_ico, shows_a_ico)

    def animate_car(self, labl, frames, img):
        try:
            frame = next(frames)
            img2 = ImageTk.PhotoImage(frame)
            self.img2 = img2
            try:
                labl.config(image=self.img2)
                self.window.update_idletasks()
                self.window.after(15, lambda: self.animate_car(labl, frames, img))
            except:
                pass
        except StopIteration:
            frames = ImageSequence.Iterator(img)
            self.window.after(1000, lambda:self.animate_car(labl, frames, img))
    

    
    ## ==> Show all cars info page
    def show_Info(self):       
        if self.datas:
            self.menuBar.entryconfig(" Home ", state = NORMAL)

            self.display_frame = Frame(self.window)
            self.display_frame.grid(row=0, column=0, sticky="nsew")

            back_btn = Button(self.display_frame, image=self.back_ico, text=" Back", compound="left", width=100, height=20, font=('Consolas', 11, 'bold'), background="lightblue", activebackground="lightblue", command=lambda: [self.start_frame.tkraise(), self.display_frame.destroy(), self.dis_menu(" Home ")])
            back_btn.pack(anchor=W, padx=10, pady=10, ipady=5)

            self.data_info = Label(self.display_frame, text="", font=("", 14, "bold"))
            self.data_info.pack(pady=5)

            # tree view shows columnwide so I created yscroll only
            self.tree = ttk.Treeview(self.display_frame, show="headings", style="Treeview")
            self.tree.pack(padx=20, pady=20, fill="both", expand=True)
            yscroll = Scrollbar(self.tree, relief="sunken", orient='vertical', command=self.tree.yview)

            # 13/6/24 added xscrollbar cuz when it shows datas first time, it dont show all columns
            xscroll = Scrollbar(self.tree, relief="sunken", orient="horizontal", command=self.tree.xview)
            yscroll.pack(side=RIGHT, fill=Y)
            xscroll.pack(side=BOTTOM, fill=X)
            self.tree.config(yscrollcommand=yscroll.set)
            self.tree.config(xscrollcommand=xscroll.set)

            self.tree.bind("<Button-3>", lambda event: self.click_n_show(self.tree, event))
            self.display_info()

            self.tree.bind("<Motion>", lambda event: self.highlight2(self.tree, event))

        else:
            self.info_labl.config(image=self.warn_box, text=f"\nYour data is {'invalid' if self.datas else 'empty'}.\nFile is not loaded yet!", compound="top", fg="red")
    
    def display_info(self):

        with open(self.file, 'r', newline='') as file:  #can use self.datas
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header row
            self.tree.delete(*self.tree.get_children())  # Clear the current data

            brands= [] # to display number of brands
            self.tree["columns"] = header
            for col in header:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)
            
            # for row colors
            self.tree.tag_configure("oddrow", background="lightblue")
            self.tree.tag_configure("evenrow", background="blanched almond")

            count = 0
            for i, row in enumerate(self.sorted_data):
                tags = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tag=tags)
                count += 1 # to count rows
                if row[0] not in brands:
                    brands.append(row[0]) # can  also use this line only and later use set() to remove duplicates
            self.data_info.config(text=f"There are {count} {self.__class__.__name__} with {len(brands)} different types.")

        
    ## ==> More page
    def explore_Info(self):
        if self.datas:
            self.menuBar.entryconfig(" Home ", state=NORMAL)

            # to use in search, add
            self.text_col = ["Brand", "Model", "Drive_Configuration", "Tow_Hitch"]
            self.float_col = ["Battery", "Acceleration(0-100km/h) Time"]
            self.num_col = ["Top_Speed", "Range(km)", "Efficiency(Wh/km)", "Fastcharge",\
                            "Estimated_US_Value", "Towing_capacity_in_kg", "Number_of_seats"]

            self.num = round(len(self.datas[0])/2)
            self.fst_half = self.datas[0][:self.num+1]  # to display more in 1st half
            self.scd_half = self.datas[0][self.num+1:]

            self.search_frame = Frame(self.window, background="#838B8B")
            self.search_frame.grid(row=0, column=0, sticky="nsew")
            self.search_frame.columnconfigure(0, weight=1)
            


            self.frame1 = Frame(self.search_frame, background="lightblue",borderwidth=2, relief="solid")
            self.frame1.grid(row=0, column=0, padx=10, pady=10, ipadx=10)
            self.entries = []
            # value = StringVar()
            self.up_img_a = Image.open(self._get_filepath("upload.gif"))
            self.up_img = ImageTk.PhotoImage(Image.open(self._get_filepath("upload.gif")))            
            

            for i in range(len(self.fst_half)): # 1 word length = 8 screenunit
                Label(self.frame1, text=f"{self.fst_half[i]} : ",background="lightblue", font=("Consolas", 11, "bold"),\
                       wraplength=184).grid(row=i, column=0, padx= 10,  pady=5, sticky=W)
                e = Entry(self.frame1, font=("Consolas", 12))
                e.grid(row=i, column=1, columnspan=5, pady=5, ipadx=5) # row ends at 7
                self.entries.append(e)

            for i in range(len(self.scd_half)): # add 1 to add image entry
                Label(self.frame1, text=f"{self.scd_half[i]} : ", background="lightblue", font=("Consolas", 11, 'bold')).grid(row=i, column=10, padx=10, pady=5, sticky=W)
                e = Entry(self.frame1, font=("Consolas", 12))
                e.grid(row=i, column=11, columnspan=5, pady=5, ipadx=5)
                self.entries.append(e)

            if self.isAdmin:
                up_img_btn = Button(self.frame1, image=self.up_img, text=" Upload Image", compound="left",\
                                     font=("Consolas", 11, "bold"), width=130, height=18, bg="lightblue",\
                                          command=lambda: self.upload_image(self.img_e))
                up_img_btn.grid(row=len(self.scd_half), column=10, pady=5, ipadx=5, ipady=5, padx=15, sticky=W)#, padx=20, sticky=E)
                self.gif_animation(up_img_btn, self.up_img, self.up_img_a)

                self.img_e = Entry(self.frame1, font=("Consolas", 12))
                self.img_e.grid(row=len(self.scd_half), column=11, columnspan=5, pady=5, ipadx=5)
                

            for e in self.entries[:2]:
                if e == self.entries[1] :
                    e.bind("<Button-3>", lambda event:self.popup_fill_val(self.frame1, 1, event, self.entries[0].get()))
                else:
                    e.bind("<Button-3>", lambda event:self.popup_fill_val(self.frame1, 0, event))
            
            btn_frame = Frame(self.search_frame, bg="#838B8B")
            btn_frame.grid(row=10, column=0, sticky="ns")

            opt = ["back_ico.png", "search.png", "add.png", "update.png", "delete.png"]
            self.opt_img=[]
            for i in opt:
                self.opt_img.append(ImageTk.PhotoImage(Image.open(self._get_filepath(i))))

            self.option_lst = [" Back", " Search", " Add", " Update", " Delete"]
            self.btns = [] 
            opt_a_ico = ["search-box.gif", "add-folder.gif", "edit.gif", "delete.gif"]
            self.opt_a_ico = [Image.open(self._get_filepath(img)) for img in opt_a_ico]

            if self.isAdmin:
                for i, opt in enumerate(self.option_lst):
                    btn = Button(btn_frame, image=self.opt_img[i], text=opt, width=100, height=20, compound="left", fg="black", bg="lightblue", activebackground="lightblue", font=('Consolas', 11, 'bold'), command=lambda a=i: self.process_button(a)) # I will go with i instead of opt
                    btn.grid(row=1, column=3+i*2, padx=20, ipady=5, sticky="we")#  
                    self.btns.append(btn)

                for i, btn in enumerate(self.btns[1:]):
                    self.gif_animation(btn, self.opt_img[i+1], self.opt_a_ico[i])  
            else:
                for i, opt in enumerate(self.option_lst[:2]):
                    btn = Button(btn_frame, image=self.opt_img[i], text=opt, width=100, height=20, compound="left", fg="black", bg="lightblue", activebackground="lightblue", font=('Consolas', 11, 'bold'), command=lambda a=i: self.process_button(a)) # I will go with i instead of opt
                    btn.grid(row=1, column=3+i*2, padx=20, ipady=5, sticky="we")#  
                    self.btns.append(btn)
                self.gif_animation(self.btns[1], self.opt_img[i+1], self.opt_a_ico[i]) 

            frame2 = Frame(self.search_frame, background="lightgrey", borderwidth=1)
            frame2.grid(row=17, column=0, padx=30, ipadx=3, ipady=3, pady=10, sticky="nswe")

            frame2.columnconfigure(0, weight=2)
            frame2.rowconfigure(0, weight=1)

            self.show_txt = Entry(frame2, borderwidth=2, font=("Consolas", 12), justify="center")
            self.show_txt.grid(row=0, column=0, sticky="nswe")
            
            # self.style.theme_use("default")
            # self.style.configure('Treeview.Heading', background="darkolivegreen1", font=("Consolas", 11, "bold"), rowheight=35)
            # self.style.configure('Treeview', font=("Concolas", 10, "bold"), rowheight=25)

            self.tree_search = ttk.Treeview(frame2, show="headings", height=8, style="Treeview")
            self.tree_search.grid(row=1, column=0, sticky="nswe")

            # to store row's value when one row is selected
            self.tree_search.bind("<<TreeviewSelect>>", self.store_value) 
            
            self.tree_search.bind("<Motion>", lambda event: self.highlight2(self.tree_search, event))
            self.tree_search.bind("<Button-3>", lambda event: self.click_n_show(self.tree_search, event))

            # to store treevie's selected row and , will be used to fill entry
            self.selected_lst = [] 

            xscroll= Scrollbar(frame2, orient="horizontal", command=self.tree_search.xview, highlightcolor="blue")
            yscroll= Scrollbar(frame2, orient="vertical",command=self.tree_search.yview, borderwidth=1, relief="solid",\
                                background="skyblue")
            xscroll.grid(row=2,column=0, sticky="we")#, ipadx=420)
            yscroll.grid(row=1, column=1, sticky=NS)#, ipady=120)

            self.tree_search.config(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

            # set heading row color
            style = ttk.Style()
            style.theme_use('default')  # try with different theme ('clam', etc..)
            style.configure('Treeview.Heading', background="skyblue", rowheight=20)
            
        else:
            self.info_labl.config(image=self.warn_box, text=f"\nYour data is {'invaid' if self.datas else 'empty'}.\n Please load the data!", compound="top")

    # new add feature to edit del
    def store_value(self, event):
        try:
            self.selected_lst.clear() # cleared first cuz I will store one row only
            selected_item = self.tree_search.selection()[0] # row text
            self.item_value = self.tree_search.item(selected_item, "values") # I used values to add data
            print(self.item_value)
            for item in self.item_value:
                self.selected_lst.append(item.strip())
            print(self.selected_lst)
        except Exception:
            self.tree_search.focus_set()

    # try to highlight row when hovering cursor
    def highlight2(self, tree, event): # set tree parameter to apply to different treeview
            tree.tag_configure("highlight", background="lightblue")
            item = tree.identify_row(event.y)
            tree.tk.call(tree, "tag", "remove", "highlight")
            tree.tk.call(tree, "tag", "add", "highlight", item)
    
    def click_n_show(self, tree, event):

        tp = Toplevel(self.window)
        tp.geometry("500x400")
        tp.resizable(False, False)
        tp.attributes("-toolwindow", True)

        selected_item = tree.selection()[0] # row text
        item_values = tree.item(selected_item, "values")
        brand=item_values[0].lower()

        tp.title(f"{item_values[0]}")
        tp.iconphoto(False, PhotoImage(file=self._get_filepath(brand+".png"))) #file="./Project/brands/"+brand+".png"
        
        model=item_values[1]
        price=int(item_values[-1])
        path=self._get_filepath(brand)
        img=None
        for x in os.listdir(path):
            if model == x[:-4]:
                img=ImageTk.PhotoImage(Image.open(path+"/"+x).resize((400,250)))

        tp.columnconfigure(0, weight=1)
        tp.rowconfigure(0, weight=1)
        frame = Frame(tp, background="skyblue", borderwidth=2, relief="solid")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        Label(frame, image=img, background="skyblue", cursor="hand2")\
        .grid(row=0, column=0, pady=10, sticky=NSEW)
        Label(frame, text=f"{model}  - (${price:,.0f})", background="skyblue", font=("", 12, "bold"))\
            .grid(row=1, column=0, pady=5, sticky=N)      # add ,(thousand separator) with no decimal point
        tp.mainloop()

    def upload_image(self, entry):
        file = filedialog.askopenfilename(
            initialdir="C:/User/Desktop/",
            title="Upload Image",
            filetypes = [("PNG", "*.png"), ("JPEG", "*.jpg")]
        )
        if file != "":
            entry.delete(0, END)
            entry.insert(END, file)

    def process_button(self, i):
        self.show_txt.config(state="normal", fg="black")
        self.show_txt.delete(0, END)

        # it will clear entries values list whenever button is clicked
        self.val_lst.clear() 
        # to store what we type in entry each button press
        temp_lst = [self.option_lst[i]] 
        for e in self.entries:
            if self.entries[0] == e:
                value=e.get().upper()
                self.val_lst.append(value) 
                temp_lst.append(value) 
            else:

                self.val_lst.append(e.get())
                temp_lst.append(e.get())

        if i in [1, 2]:
            if i == 1:
                self.hist_dict["Searched"] = temp_lst
            else:
                self.hist_dict["Added"] = temp_lst

        if i == 0:
            self.start_frame.tkraise()
            self.search_frame.destroy()
            self.dis_menu(" Home ")

        elif i == 1:
            # to check each entry is empty or not, 0 means empty
            show_all = 0  
            for value in self.val_lst:
                show_all += len(value)

            if show_all == 0: # that means all entry are empty(string)
                self.entries[0].focus_set()
                self.show_txt.config(fg="red")
                self.show_txt.insert(END, "Please provide at least brand name to search!")
                self.show_txt.config(state="readonly")

                # to delete columns row + rows
                self.tree_search.delete(*self.tree_search.get_children())
                self.tree_search["columns"] = () 

            else:
                self.search_Info()
                self.show_txt.config(state="readonly")

        elif i == 2:
            self.add_Info()
        elif i==3:
            # modified func 10/6/24
            if self.selected_lst:
                self.edit_directly()
            else:
                self.show_txt.config(fg="red")
                self.show_txt.insert(END, "There is no selected data to edit!")
                self.show_txt.config(state="readonly")
        else:
            if self.selected_lst:
                self.del_directly()
            else:
                self.show_txt.config(fg="red")
                self.show_txt.insert(END, "There is no selected data to delete!")
                self.show_txt.config(state="readonly")  


    def search_Info(self): 
        
        self.tree_search.delete(*self.tree_search.get_children())
        header = self.datas[0]
        self.tree_search["columns"] = header
        for col in header:
            self.tree_search.heading(col, text=col)
            self.tree_search.column(col, width=100)

        # df = pd.DataFrame(self.datas[1:], columns=self.datas[0])
        # self.numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        # self.float_columns = df.select_dtypes(include=[np.float64]).columns.tolist()
        # self.object_columns = df.select_dtypes(include=[object]).columns.tolist()

        df = pd.read_csv(self.file) 
        search_lst = [*zip(self.datas[0], self.val_lst)]
        # use to apply each type attributes respectively
        # self.text_col = ["Brand", "Model", "Drive_Configuration", "Tow_Hitch"]
        # self.float_col = ["Battery", "Acceleration(0-100km/h) Time"]
        # self.num_col = ["Top_Speed", "Range(km)", "Efficiency(Wh/km)", "Fastcharge",\
        #                  "Estimated_US_Value", "Towing_capacity_in_kg", "Number_of_seats"]

        # Initialize an empty mask
        mask = pd.Series(True, index=df.index)
        try:
            # Apply conditions from search_lst
            for col, val in search_lst:
                if val != "":
                    # For each tuple in search_lst, we update the mask by performing an element-wise AND operation (&)
                    # with the condition based on the column and search value.
                    if col in self.text_col:
                        # apply str methods
                        mask &= df[col].str.contains(val, case=False)
                    elif col == self.num_col[-1]: # means number_of_seats
                        mask &= df[col] == int(val)
                    else: # for float and int
                        mask &= df[col] <= float(val) # used float insted of int
        except Exception as e:
            print(e)

        result = df[mask]
        # chg data type to string
        result = result.astype(str)
        result_lst = result.to_numpy().tolist() # chnage it to numpy array and then to change to list , use to_numpy().tolist()

        self.show_txt.config(fg="green")
        self.show_txt.insert(END, f"{len(result_lst)} results were found!")
        self.show_txt.config(state="readonly")

        for row in result_lst:
            self.tree_search.insert("", "end", values=row)

    def add_Info(self):
        
        add_list = []
        empty = True if all(item == "" for item in self.val_lst) else False
        if empty:
            self.show_txt.config(fg="red")
            self.show_txt.insert(END, "Empty data can't be added! Please provide at least one.")
            self.show_txt.config(state="readonly")
            self.entries[0].focus_set()
        else:
            self.val_lst[-1] = 0 if self.val_lst[-1]=="" else self.val_lst[-1]
            for value in self.val_lst:
                if value == "":
                    add_list.append("")
                else:
                    add_list.append(value)

            # self.tree_search.delete(*self.tree_search.get_children())
            # header = self.datas[0]
            # self.tree_search["columns"] = header
            # for col in header:
            #     self.tree_search.heading(col, text=col)
            #     self.tree_search.column(col, width=30, anchor='w')

            # to display brand and model are must fill entries
            if add_list[0] != "" and add_list[1] != "":
                # if same brand and model name in original data, adding data can;t be done.
                if add_list[0] in [data[0] for data in self.datas[1:]] and \
                    add_list[1] in [data[1] for data in self.datas[1:]]:

                    self.show_txt.config(fg="red")
                    self.show_txt.insert("end", f"{self.datas[0][0]} : {add_list[0]}, {self.datas[0][1]} : {add_list[1]} is in your {self.__class__.__name__}.")
                    self.tree_search["columns"] = ()
                    self.show_txt.config(state="readonly")
                else:
                    # add just existing brand's models img
                    add_path = self.img_e.get()
                    add_img = add_list[1].strip()+".png"  #eg / -> model.png
                    brand_path = self._get_filepath("brands")

                    model_path = self._get_filepath("models/"+add_list[0].lower())+"/"

                    response = messagebox.askokcancel("Add", "Are you sure to add this data?")
                    if response:
                        # adding image
                        if add_list[0].lower() in [brand[:-4] for brand in os.listdir(brand_path)]:
                            try:
                                Image.open(add_path).save(model_path+add_img)
                            except:
                                if "suv" in add_img[:-4].lower():
                                    Image.open(self._get_filepath("frame_logo/suv.png")).save(model_path+add_img)
                                else:
                                    Image.open(self._get_filepath("frame_logo/car.png")).save(model_path+add_img)
                        else:
                            Image.open(self._get_filepath("frame_logo/unknown.png")).save(brand_path+add_list[0].lower()+".png") # here I also use added img as brand logo
                            try:
                                Image.open(add_path).save(model_path+add_img)
                            except:
                                if "suv" in add_img[:-4].lower():
                                    Image.open(self._get_filepath("frame_logo/suv.png")).save(model_path+add_img)
                                else:
                                    Image.open(self._get_filepath("frame_logo/car.png")).save(model_path+add_img)

                        modified_lst = []
                        # I can do the same in creating add_list
                        for i,data in enumerate(add_list):
                            if self.datas[0][i] in self.text_col:
                                if data == "":
                                    data = str("no value")
                            elif self.datas[0][i] in self.float_col:
                                try:
                                    data = float(data)
                                except:
                                    data = float(0)
                            else:
                                try:
                                    data = int(data)
                                except:
                                    data = int(0)
                            modified_lst.append(data)

                        self.datas.append(modified_lst) # if just add_list , "" wil be nan
                        self.save_datas()
                        self.show_txt.config(fg="green")
                        self.show_txt.insert(END, "Your data is added!")
                        self.show_txt.config(state="readonly")

                        self.tree_search.delete(*self.tree_search.get_children())
                        header = self.datas[0]
                        self.tree_search["columns"] = header
                        for col in header:
                            self.tree_search.heading(col, text=col)
                            self.tree_search.column(col, width=30, anchor='w')
                            
                        self.tree_search.insert("", END, values=modified_lst) # add_list
                    else:
                        self.show_txt.config(fg="black")
                        self.show_txt.delete(0, END)
                        self.tree_search.delete(*self.tree_search.get_children())
                        self.tree_search["columns"] = ()
                        
            else:  
                if add_list[0] == "": 
                   self.entries[0].focus_set()
                else:
                    self.entries[1].focus_set()
                        
                self.show_txt.config(fg="red")
                self.show_txt.insert(END, f"PLease fill both {self.datas[0][0]} and {self.datas[0][1]}!")
                self.show_txt.config(state="readonly")
                self.tree_search["columns"] = () # to prevent showing columns row only

    def edit_directly(self):
        
        # self.selected_lst # contains selected values to fill in entry
        self.index_to_ud = self.datas.index(self.selected_lst)
        self.updated_info = self.datas[self.index_to_ud][:2]# brand and model to use in info messagebox (optional)

        self.num = round(len(self.datas[0])/2)

        self.edit_frame1 = Frame(self.window, bg="#838B8B")
        self.edit_frame1.grid(row=0, column=0, sticky="nsew")
        self.edit_frame1.columnconfigure(0, weight=1)
        self.edit_frame1.rowconfigure(17, weight=0)


        self.edit_frame2 = Frame(self.edit_frame1, background="lightblue",relief="solid")
        self.edit_frame2.grid(row=0, column=0, padx=10, pady=20, ipadx=10)#,sticky="we")#, 
        
        # value = StringVar()
        self.entries1 = []
        for i in range(len(self.fst_half)):
            Label(self.edit_frame2, text=f"{self.fst_half[i]} : ",background="lightblue", font=("Consolas", 11, "bold"), wraplength=184).grid(row=i, column=0, padx= 10,  pady=5, sticky=W)
            e = Entry(self.edit_frame2, font=("Consolas", 12))
            e.insert(END, self.selected_lst[i]) # <----- 
            e.grid(row=i, column=1, columnspan=5, pady=5, ipadx=5) # row ends at 7
            self.entries1.append(e)
        # print(self.entries1)
        path = os.path.abspath(".")
        self.path = "/".join(p for p in path.split('\\'))

        img_path = f"{self.path}/models/{self.selected_lst[0].lower()}/{self.selected_lst[1]}.png"
        
        for i in range(len(self.scd_half)+1):
            # image entry
            if i == len(self.scd_half):

                up_img_btn = Button(self.edit_frame2, image=self.up_img, text=" Upload Image", compound="left", font=("Consolas", 11, "bold"), width=130, height=18, bg="lightblue", activebackground="lightblue", command=lambda : self.upload_image(self.img_e1))
                up_img_btn.grid(row=i, column=10, pady=5, ipadx=5, ipady=5, padx=15, sticky=W)#, padx=20, sticky=E)
                self.gif_animation(up_img_btn, self.up_img, self.up_img_a)
                
                self.img_e1 = Entry(self.edit_frame2, font=("Consolas", 12))
                self.img_e1.insert(END, img_path)
                self.img_e1.grid(row=i, column=11, columnspan=5, pady=5, ipadx=5)

            else:
                Label(self.edit_frame2, text=f"{self.scd_half[i]} : ", background="lightblue", font=("Consolas", 11, "bold")).grid(row=i, column=10, padx=10, pady=5, sticky=W)
                e = Entry(self.edit_frame2, font=("Consolas", 12))
                e.insert(END, self.selected_lst[self.num+1+i])
                e.grid(row=i, column=11, columnspan=5, pady=5, ipadx=5)
                self.entries1.append(e)

        self.entries[0].config(state="readonly") # make brand can't be changed
        btn_frame = Frame(self.edit_frame1, bg="#838B8B")
        btn_frame.grid(row=10, column=0, sticky="ns")

        Button(btn_frame, image=self.back_ico, text=" Back", compound="left", width=100, height=20, font=('Consolas', 11, 'bold'), background="lightblue", activebackground="lightblue", command=lambda: [self.search_frame.tkraise(), self.edit_frame1.destroy()])\
        .grid(row=1, column= 0, padx=20, pady=5, ipadx=5, ipady=5, sticky=EW)

        btn= Button(btn_frame, image=self.save_ico, text=" Save", compound="left", width=100, height=20, font=('Consolas', 11, 'bold'), background="lightblue", activebackground="lightblue", command=self.update)
        btn.grid(row=1, column=2, padx=20, pady=5, ipadx=5, ipady=5, sticky=EW)
        self.gif_animation(btn, self.save_ico, self.save_a_ico)

    def update(self):

        self.modified_lst = []
        for e in self.entries1:
            self.modified_lst.append(e.get())

        # try:
        edit_model_path = self.img_e1.get()
        edit_model_name = self.img_e1.get().split("/")[-1]
        img_path = self._get_filepath("models/"+self.selected_lst[0].lower())
        ori_model_img = [img for img in os.listdir(img_path) if img == self.selected_lst[1]+".png"]
        ori_img_path =f"{self.path}/models/{self.selected_lst[0].lower()}/{ori_model_img[0]}"

        #     # it checks the image is still same, if not replace that image
        #     if edit_model_name != ori_model_img[0] or edit_model_path != ori_img_path:
        #         if not os.path.exists("./Project/recycle_imgs"):
        #                 os.mkdir("./Project/recycle_imgs")

        #         if edit_model_name != "edit_"+ori_model_img[0]:
        #             Image.open(img_path+"/"+ori_model_img[0]).save("./Project/recycle_imgs/"+"edit_"+ori_model_img[0]) #edit  
        #             os.remove(img_path+"/"+ori_model_img[0])
        #         else:
        #             i = 0
        #             Image.open(img_path+"/"+ori_model_img[0]).save("./Project/recycle_imgs/"+"edit_"+ori_model_img[0][:-4]+str(i)+".png") #edit  
        #             os.remove(img_path+"/"+ori_model_img[0])
        #             i+= 1

        #         try:
        #             Image.open(edit_model_path).save(img_path+"/"+ori_model_img[0]) # edited
        #         except:
        #             if "suv" in edit_model_name[:-4]:
        #                 Image.open("./Project/frame_logo/suv.png").save(img_path+"/"+ori_model_img[0])
        #             else:
        #                 Image.open("./Project/frame_logo/car.png").save(img_path+"/"+ori_model_img[0])  
        #     else:
        #         print("The image doesn't change")
        # except:
        #     pass


        frame2 = Frame(self.edit_frame1, background="lightgrey", relief="solid", borderwidth=1)
        frame2.grid(row=17, column=0, columnspan=30, rowspan=8, padx=30, sticky="nswe")# ipadx=3, ipady=3,
        # # frame2.grid_propagate()
        frame2.columnconfigure(1, weight=1)
        frame2.rowconfigure(1, weight=0)

        diff = set(enumerate(self.modified_lst)).difference(set(enumerate(self.selected_lst))) 
        same = self.modified_lst == self.selected_lst

        if same and edit_model_path == ori_img_path: # edited
            # if all modified datas and selected datas are same, just go save and stright back 
            frame2.destroy()
            self.notify()

        else:
            self.cancel_btn = Button(frame2, image=self.cancel_ico, text=" Cancel", compound="left", width=100, height=20, font=('Consolas', 11, 'bold'), background="lightblue", activebackground="lightblue", command=frame2.destroy)
            self.cancel_btn.grid(row=0, column=1, ipadx=5, ipady=5, sticky=NW)#, padx=25

            # self.confirm_ico = ImageTk.PhotoImage(Image.open("./Project/frame_log/confirm.png"))
            self.confirm_btn = Button(frame2, image=self.confirm_ico, text=" Confirm", compound="left", width=100, height=20, font=('Consolas', 11, 'bold'), background="lightblue", activebackground="lightblue", command=self.notify)
            self.confirm_btn.grid(row=0, column=1, ipadx=5, ipady=5, sticky=NE)# padx=5,

            self.gif_animation(self.confirm_btn, self.confirm_ico, self.confirm_a_ico)

            self.edit_info = Text(frame2, wrap=None, font=("Consolas", 12), height=11, relief="solid", borderwidth=1)
            self.edit_info.grid(row=1, column=1, sticky="nsew")
            yscroll= Scrollbar(frame2, orient="vertical", relief="solid", borderwidth=2, command=self.edit_info.yview, activebackground="skyblue")
            yscroll.grid(row=1, column=2, sticky=E+NS)
            self.edit_info.config(yscrollcommand=yscroll.set)

            self.edit_info.delete(1.0, END) # I cleared text although it will destroy and recreate it

            self.edit_info.tag_configure("original_val", foreground="red")
            self.edit_info.tag_configure("modified_val", foreground="green")

            self.edit_info.insert(1.0, "You are going to do following changes..\n\n")

            for i in diff: # eg. i = (2, '57') like (column_index, its value)
                self.edit_info.insert(END, f"{self.datas[0][i[0]]} --> ")
                self.edit_info.insert(END, f" {self.selected_lst[i[0]]} ", "original_val")
                self.edit_info.insert(END, " with ")
                self.edit_info.insert(END, i[1], "modified_val", "\n")

            # for img
            self.edit_info.insert(END, ori_model_img[0], "original_val")
            self.edit_info.insert(END, " with ")
            self.edit_info.insert(END, edit_model_name, "modified_val", "\n")

            self.hist_dict["Updated"] = self.edit_info.get(3.0, END) # optional dict

    def notify(self):
        noti = messagebox.showinfo("FYI", f"You have updated {self.updated_info[0]}'s {self.updated_info[1]} infos!")
        if noti:
            try:
                edit_model_path = self.img_e1.get()
                edit_model_name = self.img_e1.get().split("/")[-1]
                img_path = self._get_filepath("models/"+self.selected_lst[0].lower())
                ori_model_img = [img for img in os.listdir(img_path) if img == self.selected_lst[1]+".png"]
                ori_img_path =f"{self.path}/models/{self.selected_lst[0].lower()}/{ori_model_img[0]}"

                # it checks the image is still same, if not replace that image
                if edit_model_name != ori_model_img[0] or edit_model_path != ori_img_path:
                    if not os.path.exists(self._get_filepath("recycle_imgs")):
                            os.mkdir(os.getcwd()+"/recycle_imgs")

                    if edit_model_name != "edit_"+ori_model_img[0]:
                        Image.open(img_path+"/"+ori_model_img[0]).save(self._get_filepath("recycle_imgs")+"/edit_"+ori_model_img[0]) #edit  
                        os.remove(img_path+"/"+ori_model_img[0])
                    else:
                        i = 0
                        Image.open(img_path+"/"+ori_model_img[0]).save(self._get_filepath("recycle_imgs")+"/edit_"+ori_model_img[0][:-4]+str(i)+".png") #edit  
                        os.remove(img_path+"/"+ori_model_img[0])
                        i+= 1
                        
                    try:
                        Image.open(edit_model_path).save(img_path+"/"+ori_model_img[0]) # edited
                    except:
                        if "suv" in edit_model_name[:-4]:
                            Image.open(self._get_filepath("frame_logo/suv.png")).save(img_path+"/"+ori_model_img[0])
                        else:
                            Image.open(self._get_filepath("frame_logo/car.png")).save(img_path+"/"+ori_model_img[0])  
                else:
                    print("The image doesn't change")
            except:
                pass

            self.datas[self.index_to_ud] = self.modified_lst # chg values and 
            self.save_datas()     # save
            self.search_Info() # to show existing data after updating

        self.edit_frame1.destroy()
        self.search_frame.tkraise()

    def del_directly(self):
        del_list = []
        selected_lines = self.tree_search.selection()
        for x in selected_lines:
            lst = [*self.tree_search.item(x, "values")] # unpacked it as it returns tuple
            del_list.append(lst)
        # print(del_list)
        
        response = messagebox.askyesno("Checking!",f"You selected {len(del_list)} rows to delete.\n Are you sure to delete?")
        if response:
            for x in del_list:
                self.datas.remove(x)
                path = self._get_filepath("models/")

                try:
                    # to delete images
                    model_path = path+x[0].lower()+"/"+x[1]+".png"
                    if not os.path.exists(self._get_filepath("recycle_imgs")):
                        os.mkdir(os.getcwd()+"/recycle_imgs")

                    Image.open(model_path).save(self._get_filepath("recycle_imgs/")+"del_"+x[1]+".png")
                    os.remove(model_path)  

                except FileNotFoundError:
                    print(f"Image not found: {model_path}")
                except Exception as e:
                    print(f"Error opening image: {e}")

                except:
                    print("It's image doesn't exist")             


            self.hist_dict["Delected"] = [x for x in del_list] 
            self.save_datas()
            complete = messagebox.showinfo("Completed!", f"You delected {len(del_list)} rows.")
            if complete:
                self.tree_search.delete(*self.tree_search.get_children())
                # self.tree_search["columns"] = ()
                self.search_Info() # to show the existing data after deleting
    
    # for popup fill
    def set_value(self, value, index, frame):
        if frame == self.frame1:
            if index == 0:
                self.entries[0].delete(0, END) # can set self.entries[index]
                self.entries[0].insert(0, value)
            else:
                self.entries[1].delete(0, END)
                self.entries[1].insert(0, value)
        else: 
            pass

    def popup_fill_val(self, frame, index, event, ent1_val=None): # it was a bit messy cuz I wrapped some funcs in it

        self.menu3 = Menu(frame, tearoff=0)
        if ent1_val:
            self.fill_val = [row[1] for row in self.datas if ent1_val in row]
        else:
            self.fill_val=set(row[index] for row in self.datas[1:])  # I used set() to get unduplicated data

        for value in self.fill_val:
            self.menu3.add_command(label=value, command=lambda v=value, i=index: self.set_value(v, i, frame))

        try:
            self.menu3.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu3.grab_release()


    ## raw funcs
    # to reset data and revert to changed data
    def chg_option(self, event):
        # frame = self.start_frame #, self.brands_main_frame, self.search_frame]:
        popup = Menu(self.start_frame, tearoff=0)
        popup.add_command(label="")
        popup.add_command(label="Reset", command=self.reset_data)
        popup.add_command(label="Revert", command=self.revert_data)

        if self.datas == self.ori_data:
            popup.entryconfig(0, label="The data are in intact.", state="disabled")
            popup.entryconfig("Revert", state="disabled")
            popup.entryconfig("Reset", state="disabled")
        else:
            popup.entryconfig(0, state="normal")
            popup.entryconfig(0, label="The data had been modified!", state="disabled")
            popup.entryconfig("Reset", state="normal")
            popup.entryconfig("Revert", state="normal")
        popup.tk_popup(event.x_root, event.y_root)

    def reset_data(self): #reset the current data to 
        response = messagebox.askokcancel("Reset", "Do you want to reset current data?")
        print(self.datas == self.ori_data)
        if response:
            self.datas = self.ori_data
            self.sorted_data = self.ori_data
            self.search_Info()
            with open(self.file, "w", newline="") as f:
                reWriter = csv.writer(f)
                reWriter.writerows(self.datas)

    def revert_data(self):
        print(self.datas == self.ori_data)
        for i, data in enumerate(self.ori_data):
            if data != self.datas[i]:
                print(data)

    # Save Data
    def save_datas(self):
        with open(self.file, 'w', newline='') as f:
            reWriter = csv.writer(f)
            reWriter.writerows(self.datas)
        # restore self.datas with updated data without reloading file agian
        with open(self.file, newline='') as file:
            csv_reader = csv.reader(file)
            self.datas = [row for row in csv_reader]
            self.sorted_data = sorted(self.datas[1:], key=lambda a: (a[0], a[1]))
        
        with open(self._get_filepath("log.txt"), "a") as l:
            for x, value in self.hist_dict.items():
                l.write(x +" - " + str(value) + "\n")

    
    def show_cars_info_ico(self):
        # self.window.iconphoto(True, PhotoImage(file="./Project/frame_logo/win_logo.png"))
        # self.window.title("Ninjas EV Info Management System") # 14/6/24 change ico and title back to normal cuz I change in models frame

        if self.datas:
            self.dis_menu(" Info ")

            self.brands_main_frame = Frame(self.window, bg="#838B8B")
            self.brands_main_frame.grid(row=0, column=0, sticky="nsew")
            self.brands_main_frame.columnconfigure(0, weight=1)

            self.brands_main_frame.tkraise() # (optional)Even if we don't add this, it works as intended
            Button(self.brands_main_frame, image=self.back_ico, text=" Back", compound="left", width=100, height=20, font=('Consolas', 11, 'bold'), background="lightblue", activebackground="lightblue", command=lambda: [self.start_frame.tkraise(), self.brands_main_frame.destroy(), self.dis_menu(" Home ")])\
                .grid(row=0, column=0, padx=5, pady=5, ipady=5, sticky="w")

            brands_path = self._get_filepath("brands/")
            self.cars_img = [img for img in os.listdir(brands_path)]

            self.ico_frame = Frame(self.brands_main_frame, bg="#838B8B", relief="groove")
            self.ico_frame.grid(row=1, column=0, sticky="n")

            names = [name[:-4].upper() for name in self.cars_img]
            self.images = [PhotoImage(file=brands_path+image) for image in self.cars_img]
            a_img = [Image.open(brands_path+image) for image in self.cars_img] # to add rotating image

            for i, car in enumerate(self.images):
                label =Label(self.ico_frame, image=car, background="skyblue", relief="groove", cursor="hand2")
                label.grid(row=i//3, column= i%3, ipadx=10, ipady=40, sticky="nswe")#  padx=10, pady=5,
                label.bind("<Button-1>", lambda event,a=i: self.show_icon(names[a], event))

                label.bind("<Enter>", lambda event, lab=label: self.ico_hover(lab, event))
                label.bind("<Leave>", lambda event, lab=label: self.ico_hover_off(lab, event))
        else:
            self.info_labl.config(image=self.warn_box, text="\nYour data is empty.\n File is not loaded yet!")


    def ico_hover(self, labl, event):
        labl["relief"] = "raised" 
    def ico_hover_off(self, labl, event):
        labl["relief"] = "groove"

    def show_icon(self,name, event):
        self.brands_main_frame.grid_forget()
        self.name = name
        
        self.ico_main_frame = Frame(self.window, bg="#838B8B")
        self.ico_main_frame.grid(row=0, column=0, sticky="nwse")
        self.ico_main_frame.columnconfigure(1, weight=1) #7
        
        models_count = len([row[1] for row in self.datas[1:] if name in row])

        self.back_btn = Button(self.ico_main_frame, image=self.back_ico, text=" Back", compound="left", width=100, height=20, font=('Consolas', 11, 'bold'), background="lightblue", activebackground="lightblue",
                                command=lambda: [self.pause_slideshow(), self.ico_main_frame.destroy(), self.show_cars_info_ico()])   # need to cancel after callbacks first, if not it will keep running although it was destroyed
        self.back_btn.grid(row=0, column=0, padx=5, pady=5, ipady=5, sticky=W)                                             

        self.img3 = ImageTk.PhotoImage(Image.open(self._get_filepath("brands/")+self.name.lower()+".png").resize((30, 30)))
        self.brand_name = Label(self.ico_main_frame, image = self.img3, compound="left", text=f"{self.name} ({models_count})", fg="white", bg="#838B8B", font=('', 12, 'bold'))
        self.brand_name.grid(row=0, column=1, padx=5, pady=5, sticky=N) #7

        path = self._get_filepath("models/") + name.lower()+"/"
        self.load_images(path)
        self.img_counter = 0
        self.action_on = False # to toggle button
        self.image_display()           


    def image_display(self):

        self.schedule_next_image() # got it right , I think I have to put it in image displaying frame
        self.model = [row for row in self.datas[1:] if self.img_modl[self.img_counter][1] in row] # [[]] retrieve row

        self.menuBar.entryconfig(" Home ", state="disabled")
        self.menuBar.entryconfig(" Info ", state="disabled")        

        # here I change the window's icon and title with selected brand's logo and name temporarily
        # self.window.iconphoto(True, PhotoImage(file="./Project/brands/"+self.name.lower()+".png"))
        # self.window.title(self.name)

        self.ico_frame1 = Frame(self.ico_main_frame, background="skyblue")
        self.ico_frame1.grid(row=1, column=1, sticky="n") # 7
        self.ico_frame1.columnconfigure([1, 2], weight=1) # 7, 8

        self.ico = Label(self.ico_frame1, image=self.img_modl[self.img_counter][0], background="skyblue", cursor="hand2")
        self.ico.grid(row=1, column=1, pady=10, sticky=NSEW) # 

        # self.action_on = False # to toggle button
        self.ico.bind("<Button-1>", lambda event: self.img_info())
 
        self.back_arrow = PhotoImage(file=self._get_filepath("frame_logo/back.png"))
        Button(self.ico_frame1, text=" < ", image=self.back_arrow, compound="none",background="skyblue", borderwidth=0, activebackground="skyblue", cursor="hand2", command=self.prev_ico).grid(row=2, column=0, padx=5, ipadx=5, ipady=5, sticky=W)
        
        self.ico_name = Label(self.ico_frame1, text=f"{self.img_counter+1}.   {self.img_modl[self.img_counter][1]} ( ${int(self.model[0][-1]):,.0f} )", background="skyblue", font=7)
        self.ico_name.grid(row=2, column=1, sticky="n") 

        self.next_btn = PhotoImage(file=self._get_filepath("frame_logo/next.png"))
        Button(self.ico_frame1, text=" > ", image=self.next_btn, compound="none", background="skyblue", borderwidth=0, activebackground="skyblue", cursor="hand2", command=self.next_ico).grid(row=2, column=2, padx=5, ipadx=5, ipady=5, sticky=E)

        self.txt_frame = Frame(self.ico_main_frame, width=80, borderwidth=2, relief="solid", background="skyblue")
        self.txt_frame.grid(row=5, column=5)
        
        for i, column in enumerate(self.datas[0][1:7]):
            Label(self.txt_frame, text=column, justify='left',background="skyblue", font=("Helvectica", 10, "bold")).grid(row=i , column=0, sticky=W, padx=5, pady=5)
            Label(self.txt_frame, text=f"- {self.model[0][i+1]}", justify='left',background="skyblue", wraplength=100, font=("Helvectica", 10, "bold")).grid(row=i, column=1, sticky=W, padx=20,pady=5)
          
        for i, column in enumerate(self.datas[0][7:]):
            Label(self.txt_frame, text=column, background="skyblue", font=("Helvectica", 10, "bold")).grid(row=i, column=3, sticky=E, padx=10, pady=5)
            Label(self.txt_frame, text=f"- {self.model[0][7:][i]}", justify='left', background="skyblue", font=("Helvectica", 10, "bold")).grid(row=i, column=4, sticky=W, pady=5)
        
        self.txt_frame.grid_forget()
        self.ico_main_frame.update_idletasks()

    def img_info(self):
        self.action_on = not self.action_on # toggling using boolean
        if self.action_on:
            self.txt_frame.grid(row=5, column=1, ipadx=30, pady=5)
            self.pause_slideshow()
        else:
            self.txt_frame.grid_forget()
            self.resume_slideshow()

    def pause_slideshow(self):
        # Cancel the scheduled image change
        if self.after_id:
            self.window.after_cancel(self.after_id)
            self.after_id = None

    def resume_slideshow(self):
        # Schedule the next image change
        if not self.after_id:
            self.after_id = self.window.after(1800, self.next_ico)

    def schedule_next_image(self):
        # Automatically change image after %ms
        self.after_id = self.window.after(1800, self.next_ico) # 1.8s


    def next_ico(self):

        self.pause_slideshow() # if it isn't added, the speed faster and got some bug
        self.img_counter += 1
        if self.img_counter == len(self.img_modl):
            self.img_counter = 0

        self.ico_frame.destroy()
        self.txt_frame.destroy()
        self.image_display() 
        self.ico_main_frame.update_idletasks()

    def prev_ico(self):

        self.pause_slideshow() # need to pause first
        if 0 < self.img_counter < len(self.img_modl):
            self.img_counter -= 1
        else:
            self.img_counter = len(self.img_modl) - 1

        self.ico_frame.destroy()
        self.txt_frame.destroy()
        self.image_display() # 6/3/24
        # add this not to cause frames overlapping, but it still does
        self.ico_main_frame.update_idletasks() 


    def load_images(self, path):
        images_dir = os.listdir(path)
        images = []
        model_names = []
        for image in images_dir:
            
            images.append(ImageTk.PhotoImage(Image.open(path+image).resize((380,230))))
            model_names.append(image[:-4])
        self.img_modl = [*zip(images, model_names)]

    @lru_cache(None) # to use cache for filepath
    def _get_filepath(self, file_path): # this must be the last
        abs_path = os.path.abspath(".") # return absolute file path with basename (like DCS) eg. C:\..\DCS
        cwd = os.getcwd()

        if os.path.exists(abs_path + f"/{file_path}"): # check file exists in current working directory
            return abs_path+f"/{file_path}" # if we want to use \, we must use escaping like \\
                
        else:
            # listing sub folders in cwd, os.scandir() will give all (files+folders)
            sub_folders = [f.name for f in os.scandir(os.path.abspath(".")) if f.is_dir()]
            for sf in sub_folders:
                if os.path.exists(abs_path + f"/{sf}/{file_path}"):
                    return abs_path + f"/{sf}/{file_path}"
                else:
                    second_dir = abs_path+'/'+sf
                    
                    subs = [f.name for f in os.scandir(os.path.abspath(second_dir)) if f.is_dir()]
                    for sf2 in subs:
                        if os.path.exists(second_dir + f"/{sf2}/{file_path}"):
                            return abs_path + f"/{sf}/{file_path}"


if __name__ == "__main__":
    evcar = EVcars()
    evcar.window.mainloop()