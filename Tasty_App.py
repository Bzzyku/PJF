import os
import sqlite3
import sys
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread, Signal, Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
import Tasty_Api_Result
from typing import Dict
from Tasty_Api_Result import Exercise,  Type_Sex, Type_Goal, Type_Activity_Level, CreateUser
from datetime import datetime
numbers = list(range(1, 101))
numbers = [str(number) for number in numbers]

class Create_User_Thread(QThread):
    user_calculated = Signal(dict)

    def __init__(self,name: str, surname: str, weight: float, height:float, sex: str, age: int):
        super().__init__()
        self.name = name
        self.surname = surname
        self.weight = weight
        self.height = height
        self.sex = sex
        self.age = age

    def run(self):
        CreateUser_Instance = CreateUser("neo4j+s://d0d8e374.databases.neo4j.io", 'neo4j','qwertyuiop')
        result = CreateUser_Instance.create_user(name=self.name, surname=self.surname, weight=self.weight, height=self.height, gender=self.sex, age=self.age)
        CreateUser_Instance.close()
        self.user_calculated.emit(result)

class Create_Exercise_Thread(QThread):
    exercise_calculated = Signal()

    def __init__(self,exercise, reps, weight, series, data):
        super().__init__()
        self.exercise = exercise
        self.reps = reps
        self.weight = weight
        self.series = series
        self.data = data

    def run(self):
        CreateUser_Instance = CreateUser("neo4j+s://d0d8e374.databases.neo4j.io", 'neo4j','qwertyuiop')
        result = CreateUser_Instance.create_exercise(exercise=self.exercise, reps=self.reps, weight=self.weight, series=self.series, data=self.data)
        CreateUser_Instance.close()
        self.exercise_calculated.emit()
class Orm_Thread(QThread):
    orm_calculated = Signal(float)

    def __init__(self, weight_lifted: float, reps: int):
        super().__init__()
        self.weight_lifted = weight_lifted
        self.reps = reps

    def run(self):
        gym_calculator_instance = Tasty_Api_Result.gym_calculator()
        result = gym_calculator_instance.orm(weight_lifted=self.weight_lifted, reps=self.reps)
        self.orm_calculated.emit(result['result'])
class Calculate_Macronutrients_Thread(QThread):
    macronutrients_calculated = Signal(dict)
    bmr_calculated = Signal(dict)
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
        result_2 = gym_calculator_instance.bmr(self.weight, self.height, self.age, self.sex)
        self.macronutrients_calculated.emit(result)
        self.bmr_calculated.emit(result_2)
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
        self.window.Push_Button_Calculate_Orm.clicked.connect(self.on_push_button_calculate_orm)
        self.window.Push_Button_Create_User.clicked.connect(self.on_push_button_create_user)
        self.window.Push_Button_Create_Exercise.clicked.connect(self.on_push_button_create_exercise)

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
        self.thread.bmr_calculated.connect(self.on_bmr_calculated)
        self.thread.start()
    def on_push_button_calculate_orm(self):
        try:
            weight_lifted = float(self.window.Line_Edit_Weight_Lifted.text())
            reps = int(self.window.Line_Edit_Reps.text())
        except ValueError:
            return
        self.thread = Orm_Thread(weight_lifted=weight_lifted, reps=reps)
        self.thread.orm_calculated.connect(self.on_orm_calculated)
        self.thread.start()
    def on_push_button_create_user(self):
        name = str(self.window.Line_Edit_Name_User.text())
        surname = str(self.window.Line_Edit_Surname_User.text())
        weight = float(self.window.Line_Edit_Weight_User.text())
        height = float(self.window.Line_Edit_Height_User.text())
        sex = str(self.window.Line_Edit_Sex_User.text())
        age = int(self.window.Line_Edit_Age_User.text())
        self.thread = Create_User_Thread(name=name, surname=surname, weight=weight, height=height, sex=sex, age=age)
        self.thread.user_calculated.connect(self.on_user_calculated)
        self.thread.start()
    def on_push_button_create_exercise(self):
        exercise = str(self.window.Line_Edit_Exercise_User.text())
        reps = int(self.window.Line_Edit_Reps_User.text())
        weight = float(self.window.Line_Edit_Weight_User.text())
        series = int(self.window.Line_Edit_Series_User.text())
        data = datetime.now()
        self.thread = Create_Exercise_Thread(exercise=exercise, reps=reps, weight=weight, series=series, data=data)
        self.thread.exercise_calculated.connect(self.on_exercise_calculated)
        self.thread.start()
    def on_orm_calculated(self, result):
        self.window.Qlabel_Orm.setText(f"Prawdopodobnie jesteś w stanie podnieść\n{str(result)} kg na jedno powtórzenie")
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

    def on_bmr_calculated(self, result_2):
        self.window.Line_Edit_Bmr.setText(str(result_2['result']))
    def on_user_calculated(self, result):
        msg = QMessageBox()
        msg.setText('Dodano Użytkownika')
        msg.exec()
    def on_exercise_calculated(self):
        msg = QMessageBox()
        msg.setText('Dodano Ćwiczenie')
        msg.exec()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec())
