import re

class Ai:
    def __init__(self, code="", example=""):
        self.original_code = code.strip()
        self.example = example.strip()
        self.converted_code = ""
        self.inputs = []
        self.user_code = ""
        self.process()

    def process(self):
        lines = self.original_code.splitlines()
        input_counter = 1
        converted_lines = []

        for i, line in enumerate(lines):
            line = line.strip()
            if "input(" in line:
                var_name = line.split('=')[0].strip()
                prompt_match = re.search(r'input\((.*?)\)', line)
                prompt_text = "Qiymat kiriting"
                if prompt_match:
                    prompt_raw = prompt_match.group(1)
                    prompt_text = prompt_raw.strip().strip('"').strip("'")
                self.inputs.append((prompt_text, input_counter))
                converted_lines.append(f"self.{var_name} = self.inputs[self.inputs_number[{input_counter}]].get()")
                if "int(" in line:
                    converted_lines.append(f"self.{var_name} = int(self.{var_name})")
                elif "float(" in line:
                    converted_lines.append(f"self.{var_name} = float(self.{var_name})")

                input_counter += 1
            elif line.startswith("print("):
                converted_lines.append(line.replace("print(", "self.print(self."))
            else:
                converted_lines.append(line)

        self.user_code = "\n".join(converted_lines)
        self.build_final_code()

    def build_final_code(self):
        self.converted_code += "from ForExample import MyLibrary\n"
        self.converted_code += f'myapp = MyLibrary(\n    flag=True,\n    example="{self.example}"\n)\n\n'

        for label, number in self.inputs:
            self.converted_code += f'myapp.Input("{label}", number={number})\n'

        self.converted_code += '\nuser_code = """\n'
        self.converted_code += self.user_code.strip() + '\n"""\n\n'
        self.converted_code += "myapp.main_code(user_code)\n"
        self.converted_code += "myapp.run()\n"

    def get_code(self):
        return self.converted_code
