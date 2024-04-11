from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox,
                             QRadioButton, QTextEdit, QListWidget, QLineEdit, QInputDialog)
import json


#notes = {
#    "Добро пожаловать!":{
#    "текст": "Я рада, что ты тут",
#   "теги": ["Встреча"]
#    }
#}
#with open("notes_file.json", "w", encoding = "utf-8") as file:
#    json.dump(notes, file)


with open("notes_file.json", "r", encoding="utf-8") as file:
    notes = json.load(file)

app = QApplication([])
main_win = QWidget()
main_layout = QHBoxLayout()

left_layout = QVBoxLayout()
text = QTextEdit()
left_layout.addWidget(text)

right_layout = QVBoxLayout()
text_list = QLabel("Список заметок")
right_layout.addWidget(text_list)
lists = QListWidget()
lists.addItems(notes)

right_layout.addWidget(lists)
button1 = QHBoxLayout()
button_so = QPushButton("Создать заметку")
button_del = QPushButton("Удалить заметку")
button1.addWidget(button_so)
button1.addWidget(button_del)
right_layout.addLayout(button1)
button_save = QPushButton("Сохранить заметку")
right_layout.addWidget(button_save)
text_teg = QLabel("Список тегов")
right_layout.addWidget(text_teg)
tegs = QListWidget()
right_layout.addWidget(tegs)
line = QLineEdit()
line.setPlaceholderText("Введите тег...")
right_layout.addWidget(line)
button2 = QHBoxLayout()
button_dob = QPushButton("Добавить тег")
button_otkr = QPushButton("Открепить от заметки")
button2.addWidget(button_dob)
button2.addWidget(button_otkr)
right_layout.addLayout(button2)
button_find = QPushButton("Искать замтеки по тегу")
right_layout.addWidget(button_find)

main_layout.addLayout(left_layout)
main_layout.addLayout(right_layout)


def show_note():
    name = lists.selectedItems()[0].text()
    text.setText(notes[name]["текст"])
    tegs.clear()
    tegs.addItems(notes[name]["теги"])


def add_note():
    text.clear()
    tegs.clear()
    note_name, result = QInputDialog.getText(lists, "Добавить заметку", "Название заметки")
    if result and not (note_name in notes) and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        with open("notes_file.json", "w", encoding="utf-8") as file:
            json.dump(notes, file)
        lists.addItem(note_name)
    elif note_name in notes:
        error = QMessageBox()
        error.setText("Такая записка уже есть, придумай другое название")
        error.exec_()


def del_note():
    try:
        name = lists.selectedItems()[0].text()
        del notes[name]
        with open("notes_file.json", "w", encoding="utf-8") as file:
            json.dump(notes, file)
        lists.clear()
        lists.addItems(notes)
        text.clear()
        tegs.clear()
    except:
        error = QMessageBox()
        error.setText("Дурашка, кажется ты не выбрал записку")
        error.exec_()


def save_note():
    try:
        name = lists.selectedItems()[0].text()
        notes[name]["текст"] = text.toPlainText()
        with open("notes_file.json", "w", encoding="utf-8") as file:
            json.dump(notes, file)
    except:
        error = QMessageBox()
        error.setText("Дурашка, кажется ты не выбрал записку")
        error.exec_()


def search_tag():
    tag = line.text()
    if button_find.text() == "Искать замтеки по тегу" and tag:
        notes_tag = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_tag[note] = notes[note]
        button_find.setText("Сбросить поиск")
        lists.clear()
        text.clear()
        tegs.clear()
        lists.addItems(notes_tag)
    elif button_find.text() == "Сбросить поиск":
        line.clear()
        lists.clear()
        tegs.clear()
        text.clear()
        lists.addItems(notes)
        button_find.setText("Искать замтеки по тегу")


def apps():
    try:
        name = lists.selectedItems()[0].text()
        tag = line.text()
        if not (tag in notes[name]["теги"]) and tag != "":
            notes[name]["теги"].append(tag)
            with open("notes_file.json", "w", encoding="utf-8") as file:
                json.dump(notes, file)
            line.clear()
            tegs.clear()
            tegs.addItems(notes[name]["теги"])
    except:
        error = QMessageBox()
        error.setText("Что то пошло не так")
        error.exec_()
        line.clear()


def tag_del():
    try:
        name = lists.selectedItems()[0].text()
        tag_text = tegs.selectedItems()[0].text()
        notes[name]["теги"].remove(tag_text)

        with open("notes_file.json", "w", encoding="utf-8") as file:
            json.dump(notes, file)
        tegs.clear()
        tegs.addItems(notes[name]["теги"])
    except:
        error = QMessageBox()
        error.setText("Что то пошло не так")
        error.exec_()
        line.clear()


lists.itemClicked.connect(show_note)
button_so.clicked.connect(add_note)
button_del.clicked.connect(del_note)
button_save.clicked.connect(save_note)
button_find.clicked.connect(search_tag)
button_dob.clicked.connect(apps)
button_otkr.clicked.connect(tag_del)

main_win.setWindowTitle("Умные заметки")
main_win.setLayout(main_layout)
main_win.setFixedSize(700, 600)
main_win.show()
app.exec_()