import tkinter as tk
class Myconsole:
    def __init__(self):
        self.root = tk.Tk() # Oyna yopilganda qo‘shimcha ish

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        self.text_widget = tk.Text(
            frame,
            bg="black",
            fg="lime",
            insertbackground="white",
            font=("Consolas", 12)
        )
        self.text_widget.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame, command=self.text_widget.yview)
        scrollbar.pack(side="right", fill="y")

        self.text_widget.config(yscrollcommand=scrollbar.set)

        self.printing_str = ""
        self.closed = False  # Oynaning yopilganini bildiruvchi flag

    def print_tk(self, *args, end: str = "\n"):
        if self.closed:
            return  # Agar oynani yopilgan bo‘lsa, yozishni to‘xtatamiz
        text = " ".join(str(arg) for arg in args) + end
        self.printing_str += text
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)

    def clear(self):
        if self.closed:
            return
        text = " "
        self.printing_str += text
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)
