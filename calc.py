import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QFont
import math
import re

def replace_trig(expr):
    trig_funcs = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'ln': math.log,
        'log': lambda x, base: math.log(x, base) if base else math.log(x),
        'sqrt': math.sqrt,
        'cbrt': math.cbrt,
        '!': lambda x: math.factorial(int(x)) if int(x) >= 0 else None,
        'pi': lambda: round(math.pi, 10)
    }

    for func, func_value in trig_funcs.items():
        if func == 'pi':
            expr = re.sub(rf'{func}', lambda match: str(func_value()), expr)
        elif func == '!':
            expr = re.sub(rf'\((\d+)\){func}', lambda match: str(func_value(match.group(1))), expr)
        else:
            expr = re.sub(rf'{func}\(([^\)]+)\)', lambda match: str(func_value(*[float(x) for x in match.group(1).split(',')])), expr)


    return expr

# print(replace_trig('log(2,8)*3')) #DEBUG

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)


        self.display = QLineEdit()
        self.display.setFont(QFont('jetbrains mono', 20))
        self.display.setFixedSize(600, 50)
        grid.addWidget(self.display, 0, 0, 1, 4)


        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '+', '='
        ]


        row_val = 1
        col_val = 0


        for button in buttons:
            if button == '=':
                btn = QPushButton(button)
                btn.clicked.connect(self.calculate)
                btn.setFixedSize(100, 50)
                btn.setFont(QFont('jetbrains mono', 16))
                btn.setStyleSheet('background-color: #4CAF50; color: #fff')
                grid.addWidget(btn, row_val, col_val, 1, 4)
                row_val += 1
            else:
                btn = QPushButton(button)
                btn.clicked.connect(self.append_text)
                btn.setFixedSize(100, 50)
                btn.setFont(QFont('jetbrains mono', 16))
                grid.addWidget(btn, row_val, col_val)
                col_val += 1
                if col_val > 3:
                    col_val = 0
                    row_val += 1


        self.clear_button = QPushButton('C')
        self.clear_button.clicked.connect(self.clear_display)
        self.clear_button.setFixedSize(600, 50)
        self.clear_button.setFont(QFont('jetbrains mono', 16))
        self.clear_button.setStyleSheet('background-color: #f44336; color: #ffffff')
        grid.addWidget(self.clear_button, row_val, 0, 1, 4)


        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close_window)
        self.close_button.setFixedSize(600, 50)
        self.close_button.setFont(QFont('jetbrains mono', 16))
        grid.addWidget(self.close_button, row_val + 1, 0, 1, 4)


        self.setWindowTitle('Calculator on PyQt')
        self.setGeometry(300, 300, 1024, 768)


        grid.setContentsMargins(200, 100, 200, 200)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(20)


    def append_text(self):
        button = self.sender()
        text = button.text()
        if self.display.text() == 'Error':
            self.display.setText('')
        self.display.setText(self.display.text() + text)

    def calculate(self):
        
        try:
            result = eval(replace_trig(self.display.text()))

            if result % 1 == 0:
                self.display.setText(str(int(result)))
            else:
                self.display.setText(str(result))
        except Exception as e:
            self.display.setText('Error')
            print(f"Error: {e}")

    

    def clear_display(self):
        self.display.setText('')


    def close_window(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    ex.show()
    sys.exit(app.exec_())