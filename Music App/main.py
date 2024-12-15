import pandas as pd
import keyboard
import os
import time
import getpass
import bcrypt
from termcolor import colored

#DCS : teambrainiacs

class MusicApp:

    def __init__(self, file_path):
        self.start = True
        self.file = self._get_filepath(file_path)
        self.music_df = pd.read_csv(self.file)
        self.headers = self.music_df.columns.to_list()
        self.headers.append("All")
 
        self.numeric_columns = self.music_df.select_dtypes(include="int64").columns.tolist()
        self.float_columns = self.music_df.select_dtypes(include="float64").columns.tolist()
        self.object_columns = self.music_df.select_dtypes(include="object").columns.tolist()

        self.attempt1 = 0
        self.attempt2 = 0
        
        
    def get_accounts(self):
        self.users= {}
        with open(self._get_filepath("user_accounts.txt"), "br") as f:
            for line in f:
                data = line.decode("utf-8").strip()
                uname, pw = data.split(":", 1)
                pw = pw.encode("utf-8")
                self.users[uname] = pw

    def create_account(self):
        accounts = {}
        create = True
        while create: # to control create account only once (any idea?)
            if self.attempt1 < 5:
                uname = str(input(f"\n{colored("Enter username ► ", "light_yellow")}"))
                if uname not in self.users.keys():

                    unv_pw = getpass.getpass(colored("Enter password ► ", "light_yellow"))
                    com_pw = getpass.getpass(colored("Confirm your password ► ", "light_yellow"))
                    if unv_pw == com_pw:
                        bpass = com_pw.encode("utf-8")
                        hashed = bcrypt.hashpw(bpass, bcrypt.gensalt())
                        
                        accounts[uname] = hashed                       
                        print(colored("!!! Creating account successful !!!", "green"))
                        
                        with open (self._get_filepath("user_accounts.txt"), "ba") as f: # in binary mode
                            for uname, pw in accounts.items():
                                f.write(uname.encode("utf-8") + b":" + pw + b"\n")
                    else:
                        print(colored("Unmatched password!\n", "light_red"))
                        self.attempt1 += 1
                else:
                    print(colored("Username already exists!\n", "light_red"))
                    self.attempt1 += 1
                print("-"*50)

                create = False
                self.start_pg()
            else:
                create = False
                print(colored("Sign-up Attempts limited!!!", "light_red"))
                print("-"*50)   
                self.start_pg()
    
    def logging_in(self):
        # users = [user for user in self.users.keys()]
        lock = False
        while not lock:
            if self.attempt2 < 5:
                username = str(input(f"\n{colored("Enter username ► ", "light_yellow")}"))

                if username in self.users.keys():
                    password = getpass.getpass(colored("Enter password ► ", "light_yellow")).encode("utf-8")
                    if bcrypt.checkpw(password, self.users[username]): # self.users[username] is hashed text
                        print(colored("\t\t\t!!! Log-in Successful !!!", "green"))
                        lock=True
                        keyboard.wait("enter", suppress=True)
                        print("-"*50)
                        self.main_menu()
                    else:
                        print(colored("\nWrong password!", "light_red"))
                        self.attempt2 += 1
                else:
                    print(colored("\nWrong username!", "light_red"))
                    self.attempt2 += 1
                print("-"*50)
                lock = True
                self.start_pg()

            else:
                lock = True
                print(colored("\nLog-in Attempts limited!!!", "light_red"))
                print("-"*50)
                self.start_pg()


    def start_pg(self): # currently no log-out function
        self.main = True
        self.once = True # to add animated effect only once for one log-in
        self.get_accounts()
        while self.start:
            print(colored("\n► You must log-in to access our app!\n", "blue"))

            choice = str(input(f"{colored("Sign-up", "yellow")}/{colored("Log-in", "yellow")}?  {colored("(0:exist)", "grey")} ► ")).lower()
            
            if choice in ["sign-up", "signup", "sign up"]: # same as ls_choice[0]
                self.create_account() # has 5 attempts
            elif choice in ["login", "log-in", "log in"]:
                self.logging_in() # has 5 attempts

            elif choice == "0":
                self.start = False
            
            else:
                print(colored("Invalid option!", "red"))
                print("-"*50)
                self.start_pg()

    def main_menu(self):
        while self.main:
            # print("\n\t\t\t♪ ♫ ♪ ♫ Welcome ♫ ♪ ♫ ♪\n") # alt+13 ♪  , alt+14 ♫

             # should Welcome be displayed only for the first runtime?
            if self.once:
                word = f"\n\t\t\t{colored("♪", "magenta")} {colored("♫", "cyan")} {colored("♪", "magenta")} {colored("♫", "cyan")} {colored("Welcome To Braisic", "green")} {colored("♫", "cyan")} {colored("♪", "magenta")} {colored("♫", "cyan")} {colored("♪", "magenta")}\n{colored("Here's what you can do.....", attrs=["bold"])}\n"
                for w in word:
                    if w == "\n":
                        print(w)
                    else:
                        print(w, end="", flush=True) # to display output immediately
                    time.sleep(0.03)
            else:
                print(f"\n\t\t\t{colored("♪", "magenta")} {colored("♫", "cyan")} {colored("♪", "magenta")} {colored("♫", "cyan")} {colored("Welcome To Braisic", "green")} {colored("♫", "cyan")} {colored("♪", "magenta")} {colored("♫", "cyan")} {colored("♪", "magenta")}\n") # alt+13 ♪  , alt+14 ♫
                print(colored("Here's what you can do.....\n", attrs=["bold"]))
            
            main_menu_list = ["Display All Musics", "Total Number of Musics", "Search Music", "Add Music", "Delete Music", "Update Music", "Exit"]        
            
            self.choice = self.valid_choice(main_menu_list, len(main_menu_list)) # this will  be in range(len(menu))
            
            if self.choice == 0:
                self.main = False
                print(f"\n{colored("♥♥♥♥", "red")} {colored("Thank You!", "cyan")} {colored("♥♥♥♥", "red")}") # any idea? ♥ = alt+3
                
                
            else: # to pass the keyboard waiting event for existing, any idea?
                if self.choice == 1:
                    self.show_all(self.music_df)

                elif self.choice == 2:
                    self.music_count()
                    keyboard.wait("enter", suppress=True) 

                elif self.choice == 3:
                    self.search_music()

                elif self.choice == 4:
                    self.add_music() 
                    self.save_csv(self.music_df)
                
                elif self.choice == 5:
                    self.delete_music()
                    self.save_csv(self.music_df)
                    
                elif self.choice == 6:
                    self.update_music() 
                    self.save_csv(self.music_df)
                    

    def sub_menu(self, title=""):
        # if search == False and delete == False:
        # here i copy self,headers and add Back
            copy_ls = self.headers.copy()
            copy_ls.append("Back")
            # this will be used in almost every methods
            while True:
                self.choice2 = self.valid_choice(copy_ls, len(copy_ls), title)
                if self.choice2 != None:
                    self.choice2
                    break
                else:
                    pass


    def show_all(self, df):
        print(colored("\nDisplaying music data ...\n", "yellow"))
        start = True
        first = True
        i = 0
        while start :
            try:
                # time.sleep(0.1) # important (cuz I use first to stop displaying, this isn't really necessary)
                if first:
                    print(colored(df.iloc[i:i+5].to_string(index=False, max_colwidth=30, col_space=10), "light_cyan")) # for spotify songs
                
                    if i+5 < len(df):
                        print(colored("\n► Press n for next, q for quit", "grey"))
                    else:
                        start= False
                        print(colored("\nDisplaying data has finished!", "green"))
                        break # I use break here, if not I would need to press 2 times (1 for any key and "enter")

                event = keyboard.read_event(suppress=True)
                if event.event_type == keyboard.KEY_DOWN and event.name in ['n', 'q']:
                    if event.name == 'n':
                        first = True
                        i+=5

                    elif event.name == 'q':
                        print(colored("\nDisplaying data has been stopped!", "light_red"))
                        start = False

                else:                   
                    first = False
                # delay to detect the key press, if not it might be detected 2 times(eg. if we press "n" once, it iterates next 2 loops)
                time.sleep(0.3)  # (optional) just for display, lower ms for large code

            except:
                print(colored("\nDisplaying data has been stopped!", "red"))


    
    def music_count(self):
        print(colored(f"\nThere are {len(self.music_df)} musics.", "blue"))

        for column in self.headers[:-1]:
            if "artist" in column.lower():
                count = [(artist, i) for artist, i in self.music_df[column].value_counts().to_dict().items()]
        for artist, num in count[:5]:
            print(f"{colored(num, "cyan")} songs of aritist - \'{colored(artist, "yellow")}\'")


    def add_music(self):
        print(colored("\nAdd music by...\n", attrs=["bold"]))
        # keyboard.wait("enter", suppress=True)

        self.sub_menu(title="Add") # display sub menu
        self.get_input() # get user input value upon seleted sub_menu options

        if bool(self.input_list) != False: # use like this or use if self.choice2 == 0: else     before self.get_input()
            self.convert_dtype(self.input_list) # convert data type based on original column data type(int, str, float, etc)

            # add to dataframe by creatinf dictionary and concatenate it
            new_row = {f"{self.headers[num]}": value for num, value in self.input_list}

            # index is needed cuz I'm using scalar values, index=[0] means based on rows
            self.music_df = pd.concat([self.music_df, pd.DataFrame(new_row, index=[0])], ignore_index= True)

            print(colored("One data added!", "green"))
            print()
            print(colored(self.music_df[-5:].to_string(index=False, max_colwidth=30, col_space=10), "light_cyan"))
            keyboard.wait("enter", suppress=True)


    def get_input(self, edit=False, search=False, delete=False):
        self.input_list = [] # want to return value or directly apply once the func is called?

        if self.choice2 == 0:
            return 
        
        else:
            # self.input_list = [] # want to return value or directly apply once the func is called?
            if not edit:
                if self.choice2 == len(self.headers): # this means "All"
                    for i in range(len(self.headers)-1): # self.headers has "All", so I omit it
                        if search == True and (self.headers[i] in self.numeric_columns or self.headers[i] in self.float_columns): # and "id" in self.headers[i].lower():
                            value = input(f"{colored("Enter", "yellow")} {colored(self.headers[i], "light_magenta")} {colored("between", "yellow")} ► ") # alt + 16 ►
                            value2 = input(f"{colored("and", "yellow")} ► ")
                            self.input_list.append((i, [value, value2]))
                        else:    
                            value = input(f"{colored("Enter", "yellow")} {colored(self.headers[i], "light_magenta")} ► ")
                            if value == "":
                                pass
                            else:
                                self.input_list.append((i, value))

                else:
                    if search == True:
                        for i, header in enumerate(self.headers[:-1], 1): # [:-1] for "Back" exclusive
                            if self.choice2 == i:
                                if header in self.float_columns or header in self.numeric_columns:
                                    value = input(f"{colored("Enter", "yellow")} {colored(header, "light_magenta")} {colored("between", "yellow")} ► ")
                                    value2 = input(f"{colored("and", "yellow")} ► ")
                                    self.input_list.append((i-1, [value, value2]))

                                else:
                                    value = input(f"{colored("Enter", "yellow")} {colored(header, "light_magenta")} ► ") # alt + 16 ►
                                    # if choice == header
                                    self.input_list.append((i-1, value))
                    else:              
                        for i in range(1, len(self.headers)):

                            # to fill value for other columns
                            if i != self.choice2: 
                                self.input_list.append((i-1, ""))
                            else:
                                value = input(f"{colored("Enter", "yellow")} {colored(self.headers[i-1], "light_magenta")} ► ") # ► alt + 16
                                self.input_list.append((i-1, value)) 
            else:
                # using index based
                for i, header in enumerate(self.headers[:-1], 1): # [:-1] for "Back" exclusive
                    if self.choice2 == i:
                        value = input(f"{colored("Enter", "yellow")} {colored(header, "light_magenta")} ► ")
                        # if choice == header
                        self.input_list.append((i-1, value))
                if self.choice2 == 8:
                    if delete:
                        opt = "deleting"
                    else:
                        opt = "updating"

                    print(colored(f"Sorry, we can't support {opt} all columns data right now!", "red"))
                    keyboard.wait("enter", suppress=True)


    def convert_dtype(self, ls, search=False): # this will convert data type and store in self.input_list
        new_list = []
        for i, value in ls:
            if self.headers[i] in self.numeric_columns:
                
                if search == True:
                    num_ls = []
                    for val in value:
                        try:
                            num_ls.append(int(val))
                        except:
                            num_ls.append(0)

                    if val != 0 and val =="": 
                        if all(n == 0 for n in num_ls):
                            pass
                        # else:
                        #     new_list.append((i, num_ls))
                    else:
                        new_list.append((i, num_ls))

                else:
                    try:
                        new_list.append((i, int(value))) # i think better use try except
                    except ValueError:
                        new_list.append((i, 0))

            elif self.headers[i] in self.float_columns:
                if search == True:
                    num_ls = []
                    for val in value:
                        try:
                            num_ls.append(float(val))
                        except:
                            num_ls.append(0.0)

                    if all(n == 0.0 for n in num_ls):
                        pass
                    else:
                        new_list.append((i, num_ls))

                else:        
                    try:
                        new_list.append((i, float(value)))
                    except :
                        new_list.append((i, 0.0))
                    
            else:
                if search:
                    if value == "":
                        pass
                    else:
                        new_list.append((i, str(value)) if value != "" else (i, "unknown") )
                else:
                    new_list.append((i, str(value)) if value != "" else (i, "unknown") )

        self.input_list = new_list # I think I should return new_list and reassign it to self.input_list


    def search_music(self):
        print(colored("\nSearch music by...\n", attrs=["bold"]))        
        self.sub_menu(title="Search") # display sub menu

        # this is another way to solve self.input_list = [] even after the program ends
        if self.choice2 == 0: # if we use like this , we can remove the duplicated codes from self.get_input()
            return 
        else:
            self.get_input(search=True) # get user input value upon seleted sub_menu options
            self.convert_dtype(self.input_list, search=True) # convert data type based on original column data type(int, str, float, etc)
            # print(self.input_list)
        
            # True to get all rows of the result , if we used False, no rows will be returned
            # use index to make same index with the existing DataFrame 
            search_mask = pd.Series(True, index=self.music_df.index)

            if self.input_list:
                for i, value in self.input_list:
                    if self.headers[i] in self.object_columns:
                        mask = self.music_df[self.headers[i]] == value

                        if not mask.any(): # check there is True in mask,  any() return True if it has at least on True
                            mask = self.music_df[self.headers[i]].str.contains(value, case=False)

                        search_mask &= mask

                    elif self.headers[i] in self.numeric_columns or self.headers[i] in self.float_columns:
                        search_mask &= (self.music_df[self.headers[i]] >= value[0]) & (self.music_df[self.headers[i]] <= value[1])
                        
                result_df = self.music_df[search_mask]

                if len(self.input_list) == 1:
                    sorted_df = result_df.sort_values(self.headers[self.input_list[0][0]])
                else:
                    header = [h for h in self.headers if "id" in h.lower() or "artist" in h.lower()]
                    sorted_df = result_df.sort_values(header[0])

                print(colored(f"\n{len(sorted_df)} result(s) found.", "green"))
                time.sleep(0.1)

                if len(sorted_df) > 20:
                    self.show_all(sorted_df)
                elif sorted_df.empty:
                    pass
                else:
                    # print(sorted_df.to_string(index=False, col_space=15)) # for old_music
                    print(colored(sorted_df.to_string(index=False, max_colwidth=20, col_space=15), "light_cyan")) # for spotify_songs
                keyboard.wait("enter", suppress=True) 
            else:
                print(colored("No data found!", "red"))
                keyboard.wait("enter", suppress=True) 


    def delete_music(self):
        
        print(colored("\nDelete music by...\n", attrs=["bold"]))     
        self.sub_menu(title="Delete") # display sub menu
        self.get_input(edit=True, delete=True) # get user input value upon seleted sub_menu options
        
        if bool(self.input_list) != False: 
            self.convert_dtype(self.input_list) # convert data type based on original column data type(int, str, float, etc)

            header = self.headers[self.input_list[0][0]]
            try:
                value = self.input_list[0][1].lower()
                data_col = self.music_df[header].str.lower()
            except:
                value = self.input_list[0][1]
                data_col = self.music_df[header]

            # result = self.music_df[self.music_df[header].str.lower() == value.lower()] 
            result = self.music_df[data_col == value] 
            count = len(result)
            # print(count)

            if count > 1:
                print(colored(f"\nThere are {count} results to delete.", "blue"))
                choice = str(input(f"{colored("Continue?", "light_yellow")} {colored("y", "green")}/{colored("n", "red")} ► ")).lower() # ► alt + 16
                if choice == "y":
                    # drop data
                    self.music_df = self.music_df[data_col != value]
                    # print(len(self.music_df))
                    print(colored(f"Removed {count} data!", "red"))
                    keyboard.wait("enter", suppress=True)
                    self.input_list.clear()

                elif choice == "n":
                    self.input_list.clear()
                    self.delete_music()
                else:
                    print(colored("Invalid input!", "red"))
                    keyboard.wait("enter", suppress=True)
                    self.input_list.clear()
                    self.delete_music()
                     
                    
            elif count == 1:
                print(colored("There is 1 data to delete.", "blue"))
                cont = str(input(f"{colored("Continue?", "light_yellow")} {colored("y", "green")}/{colored("n", "red")} ► ")).lower()
                
                if cont in ["y", "n"]:
                    if cont == "y":
                        self.music_df = self.music_df[data_col != value]
                        print(colored("One data deleted!", "green"))
                        self.input_list.clear() 
                        keyboard.wait("enter", suppress=True) 
                    else:
                        self.input_list.clear() # input_list is cleared in get_input()
                        self.delete_music() 
                else:
                    print(colored("Invalid input!", "red"))
                    keyboard.wait("enter", suppress=True)
                    self.input_list.clear()
                    self.delete_music()

            elif count == 0:
                print(colored("There is no matched result!", "red"))
                keyboard.wait("enter", suppress=True)
                self.input_list.clear()
                self.delete_music()

            # keyboard.wait("enter", suppress=True)   
        else:
            pass
                


    def update_music(self):

        print(colored("\nUpdate music by...\n", attrs=["bold"]))     
        self.sub_menu(title="Update") # display sub menu
        self.get_input(edit=True) # get user input value upon seleted sub_menu options

        if self.input_list: # same as self.input_list != []:
            self.convert_dtype(self.input_list) # convert data type based on original column data type(int, str, float, etc)
            
            # created here cuz self.input_list will be changed later
            col = self.headers[self.input_list[0][0]]
            # val = self.input_list[0][1]
            try:
                val= self.input_list[0][1].lower()
                data_col = self.music_df[col].str.lower()
            except:
                val = self.input_list[0][1]
                data_col = self.music_df[col]



            # will we use search function liked code or following code
            # index based (user have to input the existing data exactly)
            result = self.music_df[data_col == val] 
            
            # result = self.music_df[self.music_df[self.headers[self.input_list[0][0]]] == " " .join(x.capitalize() for x in self.input_list[0][1].split(" "))] # for spotify songs

            count = len(result)

            if count > 1:
                print(colored(f"\n There are {count} results to update.", "blue"))
                choice = str(input(colored("Do you want to update all? ", "yellow")+colored("y", "green")+"/"+colored("n", "red")+" ► ")).lower() # ► alt + 16
                if choice == "y":
                    if len(self.input_list) == 1:

                        # a bit complicated here
                        # directly put it in list
                        update_result = [(self.input_list[0][0], input(f"{colored("Update", "yellow")} {colored(self.headers[self.input_list[0][0]], "blue")} : \'{colored(self.input_list[0][1], "blue")}\' {colored("with", "yellow")} ► "))] 
                        
                        # create separate function ?
                        self.convert_dtype(update_result) # a new input_list is obtained

                        # both the row condition and the column specification to function correctly for assignments
                        # chg value "val" in column "col"
                        self.music_df.loc[data_col == val, col] = self.input_list[0][1]
                        
                        print(f"{colored(str(len(self.music_df[self.music_df[col] == self.input_list[0][1]])), "green", attrs=["bold"])} {colored("data updated!", "green")}")                        
                        print(colored(self.music_df.loc[self.music_df[col] == self.input_list[0][1]][:5], "light_cyan"))
                        keyboard.wait("enter", suppress=True)
                        self.input_list.clear()

                    else:
                        pass

                elif choice == "n":
                    self.input_list.clear()
                    self.update_music()

                else:
                    print(colored("Invalid input!", "red"))
                    keyboard.wait("enter", suppress=True)
                    self.input_list.clear()
                    self.update_music()
                    

            elif count == 1:
                print(colored("There is 1 data to update.", "blue"))
                cont = str(input(f"{colored("Continue?", "light_yellow")} {colored("y", "green")}/{colored("n", "red")} ► ")).lower()
                if cont in ["y", "n"]:
                    if cont == "y":
                        update_result = [(self.input_list[0][0], input(f"{colored("Update", "yellow")} {colored(self.headers[self.input_list[0][0]], "blue")} : \'{colored(self.input_list[0][1], "blue")}\' {colored("with", "yellow")} ► "))]
                        self.convert_dtype(update_result)

                        # chg value "val" in column "col"
                        self.music_df.loc[data_col == val, col] = self.input_list[0][1]  
                        print(colored("One data updated!\n", "green"))
                        print(colored(self.music_df.loc[self.music_df[col] == self.input_list[0][1]][-5:], "light_cyan"))
                        keyboard.wait("enter", suppress=True)
                        self.input_list.clear()  

                    else:
                        self.input_list.clear()
                        self.update_music()    

                else:
                    print(colored("Invalid input!", "red"))
                    self.input_list.clear()
                    keyboard.wait("enter", suppress=True)
                    self.update_music()
            else:
                print(colored("There is no data to update!", "red"))
                self.input_list.clear()
                keyboard.wait("enter", suppress=True)
                self.update_music()
                
            # keyboard.wait("enter", suppress=True)
        else:
            return


    def valid_choice(self, ls, end, title = "" ):

        choices = [num for num in range(end)]
        for i, m in enumerate(ls, 1):
            if i == end:
                i = 0
            print(f"{colored(i, "light_magenta")}. {m}")
            if self.once:
                time.sleep(0.3) # to hault continuous display

        try:
            choice = int(input(f"\n{colored(f"Choose {title} option", "yellow")}({colored(f"0-{end-1}", "light_magenta")}) ► ")) # ► alt + 16

            if choice in choices:
                self.once = False
                return choice
            else:
                print(colored("Please choose between 0 and 6!", "light_red"))
                keyboard.wait("enter", suppress=True)

        except:
            print(colored(f"Invalid! Please be sure to be number between 0 and {end}.\n", "light_red"))
            keyboard.wait("enter", suppress= True)
        self.once = False

    def save_csv(self, df):
        df.to_csv(self.file, index=False)

    def _get_filepath(self, file_path): # this must be the last
        abs_path = os.path.abspath(".") # return absolute file path with basename (like DCS) eg. C:\..\DCS

        if os.path.exists(abs_path + f"/{file_path}"): # check file exists in current working directory
            return abs_path+f"/{file_path}" # if we want to use \, we must use escaping like \\
                
        else:
            # listing sub folders in cwd, os.scandir() will give all (files+folders)
            sub_folders = [f.name for f in os.scandir(os.path.abspath(".")) if f.is_dir()]
            for sf in sub_folders:
                if os.path.exists(abs_path + f"/{sf}/{file_path}"):
                    return abs_path + f"/{sf}/{file_path}"
                

if __name__ == "__main__":
    app = MusicApp("spotify_songs.csv")
    app.start_pg()
