import tkinter as tk
import customtkinter as ctk
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class WillkommenFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.listiner = 0
        self.label_welc = ctk.CTkLabel(self, text="Willkommen beim Turnierplaner", font=("Arial",30))
        self.label_welc.grid(row=0, column=0, padx=30, pady=(30,10), sticky="ew", columnspan=100)

        self.label_2 = ctk.CTkLabel(self, text="Bitte Turniernamen eingeben: ", font=("Arial",15))
        self.label_2.grid(row=1, column=0, padx=10, pady=0, sticky="e")

        self.entry_turnier = ctk.CTkEntry(self, width=250)
        self.entry_turnier.grid(row=1, column=1, padx=10, pady=(20,30), sticky="w", columnspan=100)

        self.label_2 = ctk.CTkLabel(self, text="Gefundene Turniere: ", font=("Arial",15))
        self.label_2.grid(row=2, column=0, padx=10, pady=(0, 30), sticky="e")

        self.col_in_row = 0
        self.row_der_turniere = 2
        self.turniere = []

        for turnier_dir in os.listdir("turniere"):
            self.col_in_row += 1
            self.turniere.append(turnier_dir)
            command_func = lambda text=turnier_dir: self.turnier_name(text)

            self.turnier_dir_btn = ctk.CTkButton(self, text=turnier_dir, command= command_func)
            self.turnier_dir_btn.grid(row=self.row_der_turniere, column=self.col_in_row, padx=10, pady=(0, 30), sticky="w")
            if self.col_in_row == 4:
                self.col_in_row = 0
                self.row_der_turniere += 1

    def turnier_name(self, text):
        self.entry_turnier.delete(0, 250)
        self.entry_turnier.insert(0,text)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Turnierplaner')
        self.geometry("1000x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.willkommen_frame = WillkommenFrame(self)
        self.willkommen_frame.grid(row=0, column=0, padx=10, pady=10, sticky="")

        self.close = ctk.CTkButton(self, text="Lade Turnier", command=lambda: self.close_wilkommen_frame(self.willkommen_frame))
        self.close.grid(row=1, column=0, padx=30, pady=(0, 30), sticky="n")

    def close_wilkommen_frame(self, frame):
        frame.destroy()
        self.close.destroy()


app = App()
app.mainloop()