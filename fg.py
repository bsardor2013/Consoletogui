from ForExample import MyLibrary 
myapp = MyLibrary(
    flag=True,
    example="Kvadrat premetrini topuvchi"
)

myapp.Input("Son kiriting", number=1)

user_code = """
self.a = self.inputs[self.inputs_number[1]].get()
self.a = int(self.a)
self.print(self.a * 4)
"""

myapp.main_code(user_code)

myapp.run()
