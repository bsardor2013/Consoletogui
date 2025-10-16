# __init__.py
from .console import Myconsole
import threading
from time import sleep
def console_process():
    console = Myconsole()
    console.print_tk("Console started in separate thread.")
    globals()["mc"]=console
    console.root.mainloop()

class MyLibrary:
    def __init__(self, flag=True, example=""):
        self.flag = flag
        self.example = example
        self.inputs = []
        self.inputs_number = {}
        self.main_codes = ""
        self.import_standard_libraries()
        if self.flag:
            # Konsol oynasini alohida threadda ishga tushirish
            self.console_thread = threading.Thread(target=console_process, daemon=True)
            self.console_thread.start()
        sleep(1)
        self.mc=mc
        self.import_customtkinter()
        self.Main_root()


        """
Inputs is :{flag is console open or close } {example input exaple}
The "Print" code is written differently, it is given in "Str",
as shown below
lib is the library import option used here
a=lib.input(value="This value",number=1)
myapp=Mylib
str_code=\"\"\"
myapp.a=myapp.inputs[myapp.inputs_number[1]]#here the number assigned to the previous input is written
myapp.print(myapp.a*4)
\"\"\"
myapp.run()
        """
        self.mc.print_tk("Starting main...")
        self.mc.print_tk("Loading standard libraries...")
        self.mc.print_tk("Standard libraries import successful.")
        self.mc.print_tk("CTk Root standard Ready")
        self.mc.print_tk("Please write your code like: yourApp.run()")
        self.mc.print_tk("And define inputs with Input(), and print with print()")

    def import_standard_libraries(self):
        import subprocess
        import sys

        self.subprocess = subprocess
        self.sys = sys



        
    def import_customtkinter(self):
        try:
            self.mc.print_tk("Trying to import customtkinter...")
            import customtkinter as ctk
            self.ctk = ctk
            globals()["ctk"] = ctk
            self.mc.print_tk("customtkinter imported successfully.")
        except ImportError:
            self.mc.print_tk("customtkinter not installed.")
            self.mc.print_tk("Trying to install via pip...")
            try:
                self.subprocess.check_call(["pip", "install", "customtkinter"])
                import customtkinter as ctk
                self.ctk = ctk
                globals()["ctk"] = ctk
                self.mc.print_tk("customtkinter installed and imported.")
            except Exception as e:
                self.mc.print_tk("Failed to install customtkinter. Install it manually: pip install customtkinter")
                self.mc.print_tk(f"Error: {e}")
                self.ctk = None

    def Main_root(self):
        self.mc.print_tk("Creating main application window...")
        self.app = self.ctk.CTk()
        self.scroll_frame = self.ctk.CTkScrollableFrame(self.app, width=300, height=150)
        self.scroll_frame.pack(pady=10)

        self.example_label = self.ctk.CTkLabel(self.app, text="Example:\n" + self.example)
        self.example_label.pack()
        self.mc.print_tk("Example label added.")

        self.mc.print_tk("Console toggle added.")

        if self.flag:
            self.mc.print_tk("Console auto-start is enabled.")


    def Input(self, value: str = "", number: int = 0):
        entry = self.ctk.CTkEntry(self.app, placeholder_text=value)
        entry.pack()
        self.inputs.append(entry)
        self.inputs_number[number] = len(self.inputs) - 1
        self.mc.print_tk(f"Input created: '{value}' with number {number}")

    def print(self, value):
        label = self.ctk.CTkLabel(self.scroll_frame, text=str(value))
        label.pack()
        self.mc.print_tk(f"Printed to GUI: {value}")

    def main_code(self, code: str):
        self.main_codes = code
        self.mc.print_tk("Main code set.")

    def count(self):
        self.mc.print_tk("Running main code...")
        try:
            exec(self.main_codes, {"self": self})
            self.mc.print_tk("Main code executed successfully.")
        except Exception as e:
            self.mc.print_tk(f"Error in main code: {e}")

    def run(self):
        for entry in self.inputs:
            entry.pack()
        run_button = self.ctk.CTkButton(self.app, text="Run Code", command=self.count)
        run_button.pack(pady=10)
        self.mc.print_tk("Application is running.")
        self.app.mainloop()










