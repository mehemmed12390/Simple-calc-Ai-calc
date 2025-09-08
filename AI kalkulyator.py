import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import re

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulyator")
        self.root.geometry("350x500")
        self.root.configure(bg='black')
        self.root.resizable(False, False)
        
        # Yaddaş dəyişənləri
        self.memory = 0
        self.current_input = ""
        self.result = ""
        
        # Əsas kalkulyator hissəsi
        self.create_calculator_frame()
        
        # Klaviatura bağlamaları
        self.setup_keyboard_bindings()
        
        # AI Kalkulyator pəncərəsi
        self.ai_window = None
        
    def create_calculator_frame(self):
        # Əsas çərçivə
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display
        self.display_var = tk.StringVar()
        display = tk.Entry(main_frame, textvariable=self.display_var, font=('Arial', 20), 
                          justify='right', bg='black', fg='white', insertbackground='white',
                          bd=0, highlightthickness=2, highlightcolor='gray', highlightbackground='gray')
        display.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        # Düymə çərçivəsi
        button_frame = tk.Frame(main_frame, bg='black')
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Düymə konfiqurasiyası - şəkildəki kimi
        button_config = [
            ['MC', 'MR', 'M+', 'M-', 'MS', 'M▽'],
            ['%', 'CE', 'C', '☒'],
            ['1/x', 'x²', '3π', '⋯'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '=']
        ]
        
        # Düymələri yerləşdir
        for i, row in enumerate(button_config):
            for j, text in enumerate(row):
                if text == '⋯':
                    btn = tk.Button(button_frame, text=text, font=('Arial', 14), 
                                   bg='#2F2F2F', fg='white', width=5, height=2,
                                   command=self.open_ai_calculator)
                elif text == '=':
                    btn = tk.Button(button_frame, text=text, font=('Arial', 14), 
                                   bg='#FF9500', fg='white', width=5, height=2,
                                   command=self.calculate_result)
                elif text in ['MC', 'MR', 'M+', 'M-', 'MS', 'M▽']:
                    btn = tk.Button(button_frame, text=text, font=('Arial', 12), 
                                   bg='#2F2F2F', fg='white', width=5, height=2,
                                   command=lambda t=text: self.on_button_click(t))
                elif text in ['%', 'CE', 'C', '☒', '1/x', 'x²', '3π']:
                    btn = tk.Button(button_frame, text=text, font=('Arial', 12), 
                                   bg='#2F2F2F', fg='white', width=5, height=2,
                                   command=lambda t=text: self.on_button_click(t))
                elif text in ['×', '-', '+', '.', '+/-']:
                    btn = tk.Button(button_frame, text=text, font=('Arial', 14), 
                                   bg='#2F2F2F', fg='white', width=5, height=2,
                                   command=lambda t=text: self.on_button_click(t))
                else:
                    btn = tk.Button(button_frame, text=text, font=('Arial', 14), 
                                   bg='#1C1C1C', fg='white', width=5, height=2,
                                   command=lambda t=text: self.on_button_click(t))
                
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
                button_frame.grid_columnconfigure(j, weight=1)
            button_frame.grid_rowconfigure(i, weight=1)
    
    def setup_keyboard_bindings(self):
        # Ədəd düymələri
        for digit in range(10):
            self.root.bind(str(digit), lambda event, d=digit: self.on_key_press(str(d)))
        
        # Operator düymələri
        self.root.bind('+', lambda event: self.on_key_press('+'))
        self.root.bind('-', lambda event: self.on_key_press('-'))
        self.root.bind('*', lambda event: self.on_key_press('×'))
        self.root.bind('/', lambda event: self.on_key_press('/'))
        self.root.bind('.', lambda event: self.on_key_press('.'))
        
        # Xüsusi düymələr
        self.root.bind('<Return>', lambda event: self.calculate_result())
        self.root.bind('<Escape>', lambda event: self.on_key_press('C'))
        self.root.bind('<BackSpace>', lambda event: self.on_backspace())
        self.root.bind('<Delete>', lambda event: self.on_key_press('CE'))
        
        # M xüsusi düymələri
        self.root.bind('m', lambda event: self.on_key_press('MS'))
        self.root.bind('M', lambda event: self.on_key_press('MS'))
        self.root.bind('r', lambda event: self.on_key_press('MR'))
        self.root.bind('R', lambda event: self.on_key_press('MR'))
    
    def on_key_press(self, key):
        if key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '×', '/', '.']:
            self.on_button_click(key)
        elif key == 'C':
            self.on_button_click('C')
        elif key == 'CE':
            self.on_button_click('CE')
    
    def on_backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.display_var.set(self.current_input)
    
    def on_button_click(self, char):
        if char == 'C':
            self.current_input = ""
            self.display_var.set("")
        elif char == 'CE':
            self.current_input = ""
            self.display_var.set("")
        elif char == '=':
            self.calculate_result()
        elif char == '+/-':
            if self.current_input and self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display_var.set(self.current_input)
        elif char == 'x²':
            try:
                result = float(self.current_input) ** 2
                self.current_input = str(result)
                self.display_var.set(self.current_input)
            except:
                self.display_var.set("Error")
        elif char == '1/x':
            try:
                result = 1 / float(self.current_input)
                self.current_input = str(result)
                self.display_var.set(self.current_input)
            except:
                self.display_var.set("Error")
        elif char == '3π':
            self.current_input = str(3 * math.pi)
            self.display_var.set(self.current_input)
        elif char == 'MC':
            self.memory = 0
        elif char == 'MR':
            self.display_var.set(str(self.memory))
            self.current_input = str(self.memory)
        elif char == 'M+':
            try:
                self.memory += float(self.current_input)
            except:
                pass
        elif char == 'M-':
            try:
                self.memory -= float(self.current_input)
            except:
                pass
        elif char == 'MS':
            try:
                self.memory = float(self.current_input)
            except:
                pass
        elif char == 'M▽':
            self.display_var.set(str(self.memory))
            self.current_input = str(self.memory)
        elif char == '%':
            try:
                result = float(self.current_input) / 100
                self.current_input = str(result)
                self.display_var.set(self.current_input)
            except:
                self.display_var.set("Error")
        elif char == '☒':
            self.root.quit()
        else:
            self.current_input += char
            self.display_var.set(self.current_input)
    
    def calculate_result(self):
        try:
            # × simvolunu * ilə əvəz et
            expression = self.current_input.replace('×', '*')
            result = eval(expression)
            self.current_input = str(result)
            self.display_var.set(self.current_input)
        except:
            self.display_var.set("Error")
    
    def open_ai_calculator(self):
        if self.ai_window is None or not self.ai_window.winfo_exists():
            self.ai_window = tk.Toplevel(self.root)
            self.ai_window.title("AI Kalkulyator")
            self.ai_window.geometry("500x400")
            self.ai_window.configure(bg='black')
            
            # Notebook (tablar)
            notebook = ttk.Notebook(self.ai_window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Təbii dil rejimi
            natural_lang_frame = tk.Frame(notebook, bg='black')
            notebook.add(natural_lang_frame, text="Təbii Dil")
            
            natural_lang_text = scrolledtext.ScrolledText(natural_lang_frame, height=10, 
                                                         font=('Arial', 12), bg='#1C1C1C', fg='white')
            natural_lang_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            input_frame = tk.Frame(natural_lang_frame, bg='black')
            input_frame.pack(fill=tk.X, padx=10, pady=10)
            
            natural_lang_input = tk.Entry(input_frame, font=('Arial', 12), 
                                         bg='#1C1C1C', fg='white', insertbackground='white')
            natural_lang_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            natural_lang_input.bind('<Return>', lambda e: self.process_natural_language(natural_lang_input, natural_lang_text))
            
            send_btn = tk.Button(input_frame, text="Göndər", font=('Arial', 10),
                                bg='#FF9500', fg='white', 
                                command=lambda: self.process_natural_language(natural_lang_input, natural_lang_text))
            send_btn.pack(side=tk.RIGHT)
            
            # Vahid çevirmələr
            unit_conv_frame = tk.Frame(notebook, bg='black')
            notebook.add(unit_conv_frame, text="Vahid Çevirmələr")
            
            tk.Label(unit_conv_frame, text="Çevir:", bg='black', fg='white').pack(pady=5)
            
            from_unit = tk.Entry(unit_conv_frame, font=('Arial', 12), bg='#1C1C1C', fg='white')
            from_unit.pack(pady=5)
            
            tk.Label(unit_conv_frame, text="dən:", bg='black', fg='white').pack(pady=5)
            
            unit_types = ["KM", "Mil", "Manat", "Dollar", "Kq", "Funt"]
            from_var = tk.StringVar(value=unit_types[0])
            from_dropdown = ttk.Combobox(unit_conv_frame, textvariable=from_var, values=unit_types, state="readonly")
            from_dropdown.pack(pady=5)
            
            tk.Label(unit_conv_frame, text="yə:", bg='black', fg='white').pack(pady=5)
            
            to_var = tk.StringVar(value=unit_types[1])
            to_dropdown = ttk.Combobox(unit_conv_frame, textvariable=to_var, values=unit_types, state="readonly")
            to_dropdown.pack(pady=5)
            
            convert_btn = tk.Button(unit_conv_frame, text="Çevir", bg='#FF9500', fg='white',
                                   command=lambda: self.convert_units(from_unit, from_var, to_var, result_label))
            convert_btn.pack(pady=10)
            
            result_label = tk.Label(unit_conv_frame, text="", bg='black', fg='white', font=('Arial', 14))
            result_label.pack(pady=10)
            
            # Maliyyə hesablamaları
            finance_frame = tk.Frame(notebook, bg='black')
            notebook.add(finance_frame, text="Maliyyə")
            
            tk.Label(finance_frame, text="Maaş:", bg='black', fg='white').pack(pady=5)
            salary_entry = tk.Entry(finance_frame, font=('Arial', 12), bg='#1C1C1C', fg='white')
            salary_entry.pack(pady=5)
            
            tk.Label(finance_frame, text="Aylıq xərc:", bg='black', fg='white').pack(pady=5)
            expense_entry = tk.Entry(finance_frame, font=('Arial', 12), bg='#1C1C1C', fg='white')
            expense_entry.pack(pady=5)
            
            tk.Label(finance_frame, text="Ay sayı:", bg='black', fg='white').pack(pady=5)
            months_entry = tk.Entry(finance_frame, font=('Arial', 12), bg='#1C1C1C', fg='white')
            months_entry.pack(pady=5)
            
            calculate_btn = tk.Button(finance_frame, text="Hesabla", bg='#FF9500', fg='white',
                                     command=lambda: self.calculate_savings(salary_entry, expense_entry, months_entry, finance_result))
            calculate_btn.pack(pady=10)
            
            finance_result = tk.Label(finance_frame, text="", bg='black', fg='white', font=('Arial', 14))
            finance_result.pack(pady=10)
    
    def process_natural_language(self, input_widget, output_widget):
        query = input_widget.get()
        if not query:
            return
            
        input_widget.delete(0, tk.END)
        
        output_widget.insert(tk.END, f"Siz: {query}\n")
        
        # Sadə təbii dil emalı
        if "faiz" in query or "%" in query:
            numbers = re.findall(r'\d+', query)
            if len(numbers) >= 2:
                value = float(numbers[0])
                percentage = float(numbers[1])
                result = value * percentage / 100
                response = f"AI: {value}-ın {percentage}% = {result}\n"
            else:
                response = "AI: Faiz hesablamaq üçün rəqəmləri daxil edin (məs: 200 dolların 15%-i)\n"
        elif "kvadrat kök" in query or "kökaltı" in query:
            numbers = re.findall(r'\d+', query)
            if numbers:
                value = float(numbers[0])
                result = math.sqrt(value)
                response = f"AI: √{value} = {result}\n"
            else:
                response = "AI: Kvadrat kök üçün rəqəm daxil edin (məs: 25-in kvadrat kökü)\n"
        elif "maaş" in query and ("yığ" in query or "qal" in query or "qənaət" in query):
            numbers = re.findall(r'\d+', query)
            if len(numbers) >= 2:
                salary = float(numbers[0])
                expense = float(numbers[1])
                saving = salary - expense
                
                # Ay sayını tap
                months = 1
                month_match = re.search(r'(\d+)\s*ay', query)
                if month_match:
                    months = int(month_match.group(1))
                
                response = f"AI: Aylıq qənaət: {saving} AZN. {months} ayda {saving * months} AZN yığarsınız.\n"
            else:
                response = "AI: Maaş və xərc məlumatlarını daxil edin (məs: maaşım 1200, aylıq xərc 200)\n"
        else:
            response = "AI: Sorğunuzu başa düşmədim. Zəhmət olmasa daha aydın ifadə edin.\n"
        
        output_widget.insert(tk.END, response)
        output_widget.see(tk.END)
    
    def convert_units(self, from_entry, from_unit, to_unit, result_label):
        try:
            value = float(from_entry.get())
            from_type = from_unit.get()
            to_type = to_unit.get()
            
            # Çevrilmə əmsalları
            conversions = {
                "KM": {"Mil": 0.621371},
                "Mil": {"KM": 1.60934},
                "Manat": {"Dollar": 0.59},
                "Dollar": {"Manat": 1.70},
                "Kq": {"Funt": 2.20462},
                "Funt": {"Kq": 0.453592}
            }
            
            if from_type in conversions and to_type in conversions[from_type]:
                result = value * conversions[from_type][to_type]
                result_label.config(text=f"{value} {from_type} = {result:.2f} {to_type}")
            else:
                result_label.config(text="Bu çevrilmə mümkün deyil")
        except:
            result_label.config(text="Xəta: Keçərli rəqəm daxil edin")
    
    def calculate_savings(self, salary_entry, expense_entry, months_entry, result_label):
        try:
            salary = float(salary_entry.get())
            expense = float(expense_entry.get())
            months = int(months_entry.get())
            
            savings = (salary - expense) * months
            result_label.config(text=f"{months} ay ərzində yığacağınız məbləğ: {savings:.2f} AZN")
        except:
            result_label.config(text="Xəta: Keçərli rəqəmlər daxil edin")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()