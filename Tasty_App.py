import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread, Signal, Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
import Tasty_Api_Result
from typing import Dict
from Tasty_Api_Result import gym_calculator, Tasty_App, Exercise, Bespoke_Diet_Generator, Type_Sex, Type_Goal, Type_Activity_Level

numbers = list(range(1, 101))
numbers = [str(number) for number in numbers]

class Calculate_Macronutrients_Thread(QThread):
    macronutrients_calculated = Signal(dict)

    def __init__(self, goal: str, weight: float, height: float, age: int, sex: str, activity_level: str):
        super().__init__()
        self.goal = goal
        self.weight = weight
        self. height = height
        self.age = age
        self.sex = sex
        self.activity_level = activity_level

    def run(self):
        gym_calculator_instance = Tasty_Api_Result.gym_calculator()
        result = gym_calculator_instance.calculate_macronutrient_ratios(self.goal, self.weight, self.height, self.age, self.sex, self.activity_level)
        print(result)
        self.macronutrients_calculated.emit(result)
class BmiThread(QThread):
    bmi_calculated = Signal(float)

    def __init__(self, weight, height):
        super().__init__()
        self.weight = weight
        self.height = height

    def run(self):
        calculator = Tasty_Api_Result.gym_calculator()
        result = calculator.bmi(self.weight, self.height)
        self.bmi_calculated.emit(result)

class Exercise_Thread(QThread):
    exercise_result = Signal(str)

    def __init__(self, result, categories, difficulties, muscles):
        super().__init__()
        self.categories = categories
        self.difficulties = difficulties
        self.muscles = muscles
        self.result = result
    def run(self):
        browser = Tasty_Api_Result.Exercise()
        result = browser.filter_exercises(result=self.result, category=self.categories, difficulty=self.difficulties, muscles=self.muscles)
        self.exercise_result.emit(result)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1600, 800)
        loader = QUiLoader()
        self.window = loader.load("interfejs.ui",self)
        self.show()
        Exercise_instance = Exercise()
        result = Exercise_instance.get_exercises()
        self.result = result
        self.thread = None

        self.window.Combo_Box_Type_Exercises.addItems(Exercise_instance.get_attribiutes()["categories"])
        self.window.Combo_Box_Type_Difficulties.addItems(Exercise_instance.get_attribiutes()["difficulties"])
        self.window.Combo_Box_Type_Muscles.addItems(Exercise_instance.get_attribiutes()["muscles"])
        self.window.Combo_Box_Type_Goal.addItems([Goal.value for Goal in Type_Goal])
        self.window.Combo_Box_Type_Sex.addItems([Sex.value for Sex in Type_Sex])
        self.window.Combo_Box_Type_Activity_Level.addItems([Activity_Level.value for Activity_Level in Type_Activity_Level])
        self.window.Combo_Box_Type_Age.addItems(numbers)
        # connect the button to the on_push_button_clicked method
        self.window.Push_Button_Oblicz.clicked.connect(self.on_push_button_clicked)
        self.window.Push_Button_Find_Exercise.clicked.connect(self.on_push_button_find_exercise)
        self.window.Push_Button_Calculate_Macronutrients.clicked.connect(self.on_push_button_calculate_macronutrients)

    def on_push_button_clicked(self):
        try:
            weight = float(self.window.Line_Edit_Waga.text())
            height = float(self.window.Line_Edit_Wzrost.text())
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Wprowadź poprawne wartości dla wagi i wzrostu")
            return

        self.thread = BmiThread(weight=weight, height=height)
        self.thread.bmi_calculated.connect(self.on_bmi_calculated)
        self.thread.start()

    def on_push_button_find_exercise(self):
        categories = str(self.window.Combo_Box_Type_Exercises.currentText())
        difficulties = str(self.window.Combo_Box_Type_Difficulties.currentText())
        muscles = str(self.window.Combo_Box_Type_Muscles.currentText())
        self.thread = Exercise_Thread(result=self.result, categories=categories, difficulties=difficulties, muscles=muscles)
        self.thread.exercise_result.connect(self.on_exercise_result)
        self.thread.start()

    def on_push_button_calculate_macronutrients(self):
        goal = str(self.window.Combo_Box_Type_Goal.currentText())
        weight = float(self.window.Line_Edit_Waga.text())
        height = float(self.window.Line_Edit_Wzrost.text())
        age = int(self.window.Combo_Box_Type_Age.currentText())
        sex = str(self.window.Combo_Box_Type_Sex.currentText())
        activity_level = str(self.window.Combo_Box_Type_Activity_Level.currentText())
        self.thread = Calculate_Macronutrients_Thread(goal=goal, weight=weight, height=height, age=age, sex=sex, activity_level=activity_level)
        self.thread.macronutrients_calculated.connect(self.on_macronutrients_calculated)
        self.thread.start()
    def on_bmi_calculated(self, result):
        self.window.Line_Edit_Bmi.setText(str(result))

    def on_exercise_result(self, result):
        self.window.Line_Edit_Exercises.clear()
        self.window.Line_Edit_Exercises.setText(f'<a href="{result}">{result}</a>')
        self.window.Line_Edit_Exercises.setTextFormat(Qt.RichText)
        self.window.Line_Edit_Exercises.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.window.Line_Edit_Exercises.setOpenExternalLinks(True)
    def on_macronutrients_calculated(self, result):

        self.window.Line_Edit_Calories.setText(str(result['result']['calories']))
        self.window.Line_Edit_Protein.setText(str(result['result']['protein']))
        self.window.Line_Edit_Carbs.setText(str(result['result']['carbs']))
        self.window.Line_Edit_Fat.setText(str(result['result']['fat']))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec())
