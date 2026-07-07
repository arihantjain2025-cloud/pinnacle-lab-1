import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("350x450")
        self.root.resizable(False, False)
        
        # Configure overall grid row/column weights for proper scaling
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.root.grid_columnconfigure(j, weight=1)

        # String variable to track the current expression on screen
        self.expression = ""
        
        # Display Screen Setup
        self.display_var = tk.StringVar(value="0")
        self.create_display()
        
        # Button layout mapping: (Text, Row, Column)
        buttons = [
            ('C', 1, 0), ('/', 1, 1), ('*', 1, 2), ('-', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('+', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('%', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('=', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('00', 5, 2)
        ]
        
        self.create_buttons(buttons)
        
        # Bind keyboard events for natural typing
        self.root.bind("<Key>", self.handle_keyboard)

    def create_display(self):
        """Creates the calculation display bar at the top."""
        display = tk.Entry(
            self.root, 
            textvariable=self.display_var, 
            font=("Arial", 24), 
            bd=10, 
            insertwidth=4, 
            width=14, 
            borderwidth=0,
            justify="right", 
            state="readonly",
            background="#f4f4f4"
        )
        # Span across all 4 columns
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

    def create_buttons(self, buttons):
        """Generates the grid of buttons dynamically."""
        for (text, row, col) in buttons:
            # Span '=' vertically to fill out the layout cleanly
            rowspan = 2 if text == '=' else 1
            # Span '0' horizontally to fill space
            colspan = 1 if text != '00' else 2

            # Styling definitions
            bg_color = "#f9f9f9"
            fg_color = "#000000"
            if text in ['/', '*', '-', '+', '=', '%']:
                bg_color = "#ff9500" # Orange accents for operators
                fg_color = "#ffffff"
            elif text == 'C':
                bg_color = "#d4d4d2" # Gray accent for clear string

            btn = tk.Button(
                self.root, 
                text=text, 
                font=("Arial", 16), 
                borderwidth=1,
                bg=bg_color,
                fg=fg_color,
                activebackground="#e0e0e0",
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky="nsew", padx=2, pady=2)

    def on_button_click(self, char):
        """Core logic processing button inputs."""
        if char == 'C':
            self.expression = ""
            self.display_var.set("0")
        elif char == '=':
            self.calculate_result()
        elif char == '%':
            # Handle percentage calculation
            try:
                result = str(eval(self.expression + "/100"))
                if result.endswith('.0'):
                    result = result[:-2]
                self.display_var.set(result)
                self.expression = result
            except:
                self.display_var.set("Error")
                self.expression = ""
        else:
            # Prevent leading multiple zeroes or appending to an error block
            if self.expression in ["Error", "0"]:
                self.expression = ""
            
            self.expression += str(char)
            self.display_var.set(self.expression)

    def calculate_result(self):
        """Safely evaluates the string formula expression."""
        try:
            # Using Python's built-in eval function safely on internal state string
            result = str(eval(self.expression))
            
            # Strip trailing float decimals if it is a whole integer (e.g. 5.0 -> 5)
            if result.endswith('.0'):
                result = result[:-2]
                
            self.display_var.set(result)
            self.expression = result # Save result as baseline for next chain math
        except ZeroDivisionError:
            self.display_var.set("Error")
            self.expression = ""
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def handle_keyboard(self, event):
        """Translates keyboard hits into calculator processing rules."""
        char = event.char
        if char in '0123456789+-*/.':
            self.on_button_click(char)
        elif char == '\r' or char == '=': # Enter key or equal sign keys
            self.on_button_click('=')
        elif event.keysym == 'BackSpace':
            # Slice off the last element
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")
        elif event.keysym == 'Escape':
            self.on_button_click('C')

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()