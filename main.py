from PyQt6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar,
                             QStatusBar, QMessageBox, QTextEdit)
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
from typing import Optional


class DatabaseConnection:
    """
    Connects to the database file.

    Attributes:
    database_file (str): The path to the database file.

    Methods:
    connect (self) -> Optional[sqlite3.Connection]: Connects to the database file.

    Returns:
        Optional[sqlite3.Connection]: The connection to the database, or None if the connection could not be established.
    """

    def __init__(self, database_file='/Users/dennisrotnov/Documents/Coding/Classes/Books/py_tricks/py_tricks/code/sql-gui/database.db') -> None:
        self.database_file: str = database_file

    def connect(self) -> Optional[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_file)
        return connection


class MainWindow(QMainWindow):
    """
    The MainWindow class is the main window of the student management system. It contains the menu bar, table widget, status bar, and other elements.

    The init method sets the window title, size, and creates a vertical layout for the elements. It also creates a menu bar with three menus, File and Help and Edit. The File menu contains an Add Student action, which opens the AddDialog when triggered. The Help menu contains an About action. The Edit menu contains an Edit Student action, which opens the EditDialog when triggered.

    Two buttons are created: Add Student, Search Record. The Add Student button is used to add a new student record, the Search Record button is used to search for a student record.

    A table widget is created to display the student records. The table contains four columns, ID, Name, Course, and Phone. The row headers are hidden to avoid extra indices.

    The load_data method is used to load the data from the database into the table widget.

    The cell_clicked function is triggered when a cell in the table is clicked. It adds two buttons to the status bar, "Edit Record" and "Delete Record", which allow the user to edit or delete the corresponding record in the table.

    The edit_record function is triggered when the edit button in the status bar is clicked. It opens the EditDialog, which allows the user to edit the selected record in the table.

    The delete_record function is triggered when the delete button in the status bar is clicked. It opens the DeleteDialog, which allows the user to delete the selected record in the table.

    The insert method is used to insert a new student record into the database.

    The search method is used to search for a student record in the database.

    Attributes:
    table (QTableWidget): The table widget that displays the student records.
    statusbar (QStatusBar): The status bar that displays the buttons for editing and deleting records.
    toolbar (QToolBar): The toolbar that displays the buttons for adding and searching records.
    student_id (int): The ID of the selected student record.
    student_name (str): The name of the selected student record.
    student_course (str): The course of the selected student record.
    student_phone (int): The phone number of the selected student record.

    Methods:
    cell_clicked(self) -> None: This function is triggered when a cell in the table is clicked. It adds two buttons to the status bar, "Edit Record" and "Delete Record", which allow the user to edit or delete the corresponding record in the table.
    edit_record(self) -> None: This function is triggered when the edit button in the status bar is clicked. It opens the EditDialog, which allows the user to edit the selected record in the table.
    delete_record(self) -> None: This function is triggered when the delete button in the status bar is clicked. It opens the DeleteDialog, which allows the user to delete the selected record in the table.
    load_data(self) -> None: This function loads the data from the database into the table widget.
    insert(self) -> None: This function is used to insert a new student record into the database.
    search(self) -> None: This function is used to search for a student record in the database.
    about(self) -> None: This function is triggered when the about button is clicked. It opens the about dialog box.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)  # width, height

        # HEADER AREA WITH MENU BAR
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add subitems for File menu, Self connects QAction to the MainWindow class
        add_student_action = QAction(QIcon(
            '/Users/dennisrotnov/Documents/Coding/Classes/Books/py_tricks/py_tricks/code/sql-gui/icons/add.png'), 'Add Student', self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        # Add subitems for Help menu, Self connects QAction to the MainWindow class
        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        # Quick fix for Mac if there is no Help menu showed
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Add subitems for Edit menu, Self connects QAction to the MainWindow class
        search_record_action = QAction(QIcon(
            '/Users/dennisrotnov/Documents/Coding/Classes/Books/py_tricks/py_tricks/code/sql-gui/icons/search.png'), 'Search Record', self)
        edit_menu_item.addAction(search_record_action)
        search_record_action.triggered.connect(self.search)

        # CREATE TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Phone"))
        self.table.verticalHeader().setVisible(False)  # to avoid extra(duplicate) index

        # SPECIFY CENTRAL WIDGET FOR QMAINWINDOW
        self.setCentralWidget(self.table)
        self.load_data()

        # CREATE TOOLBAR
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Using existing actions
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_record_action)

        # CREATE STATUS BAR WITH ELEMENTS
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        # statusbar.showMessage(
        #     dt.datetime.today().strftime("%A, %B %d, %Y %I:%M %p"))

        # DETECT TABLE CLICK
        self.table.clicked.connect(
            self.cell_clicked)

    def cell_clicked(self) -> None:
        """
        This function is triggered when a cell in the table is clicked. It adds
        two buttons to the status bar, "Edit Record" and "Delete Record", which
        allow the user to edit or delete the corresponding record in the table.
        """
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_record)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_record)

        children = self.findChildren(QPushButton)

        # if children:
        #     for child in children:
        #         self.statusBar.removeWidget(child)

        # Used to avoid duplicated buttons in the status bar
        if not children:
            self.statusbar.addWidget(edit_button)
            self.statusbar.addWidget(delete_button)

    def edit_record(self) -> None:
        """
        This function is triggered when the edit button in the status bar is clicked. It opens the EditDialog, which allows the user to edit the selected record in the table.
        """
        dialog: EditDialog = EditDialog()
        dialog.exec()
        self.load_data() if dialog.success else None

    def delete_record(self) -> None:
        """
        This function is triggered when the delete button in the status bar is clicked. It opens the DeleteDialog, which allows the user to delete the selected record in the table.
        """
        dialog: DeleteDialog = DeleteDialog()
        dialog.exec()
        self.load_data() if dialog.success else None

    def load_data(self) -> None:
        """
        This function loads the data from the database into the table widget.
        """
        connection = connection = DatabaseConnection().connect().cursor()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)  # to avoid duplicated data

        for row_idx, row_data in enumerate(result.fetchall()):
            self.table.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(
                    row_idx, col_idx, QTableWidgetItem(str(col_data)))

        connection.close()

    def insert(self) -> None:
        """
        This function is used to insert a new student record into the database.
        """
        dialog: InsertDialog = InsertDialog()
        dialog.exec()
        self.load_data() if dialog.success else None

    def search(self) -> None:
        """
        This function is used to search for a student record in the database.
        """
        dialog: SearchDialog = SearchDialog()
        dialog.exec()
        if dialog.success == True:
            print(dialog.data)

    def about(self) -> None:
        """
        This function is triggered when the about button is clicked. It opens the about dialog box.
        """
        dialog: AboutDialog = AboutDialog()
        dialog.exec()


class InsertDialog(QDialog):
    '''
    The InsertDialog class is used to add a new student record to the database. It contains the following elements:

    A label for each input field, such as name, course, and phone number.
    An input field for each input field, such as name, course, and phone number.
    A drop-down menu for selecting the course.
    A button to submit the form and a button to cancel the form.

    The submit function is used to insert the new student record into the database. The cancel function is used to close the dialog box.

    Attributes:
    student_name (str): The name of the selected student record.
    student_course (str): The course of the selected student record.
    student_phone (int): The phone number of the selected student record.

    Methods:
    submit(self) -> None: This function is used to insert the new student record into the database.
    cancel(self) -> None: This function is used to close the dialog box.
    '''

    def __init__(self) -> None:
        super().__init__()
        self.success: bool = False
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(280)

        # CREATE LAYOUT
        layout = QVBoxLayout()
        self.setLayout(layout)

        # CREATE LABELS
        self.label_name = QLabel("Name:")
        self.label_course = QLabel("Course:")
        self.label_phone = QLabel("Phone:")

        # CREATE INPUTS
        self.input_name = QLineEdit()
        self.input_phone = QLineEdit()

        self.input_name.setPlaceholderText("Student name")
        self.input_phone.setPlaceholderText("Studen phone number")

        # CREATE DROP DOWN MENU
        self.course_name = QComboBox()
        self.course_name.setPlaceholderText("Select Course")
        courses = ['Math', 'Physics', 'Chemistry',
                   'Biology', 'History', 'Science']
        self.course_name.addItems(courses)

        # CREATE BUTTONS
        self.button_ok = QPushButton("Submit")
        self.button_cancel = QPushButton("Cancel")
        self.button_ok.clicked.connect(self.submit)
        self.button_cancel.clicked.connect(self.cancel)

        # ADD INPUTS TO LAYOUT
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(self.label_course)
        layout.addWidget(self.course_name)
        layout.addWidget(self.label_phone)
        layout.addWidget(self.input_phone)
        layout.addStretch()
        layout.addWidget(self.button_ok)
        layout.addWidget(self.button_cancel)

    def submit(self) -> None:
        """
        This function is used to insert a new student record into the database.
        """
        try:
            name: str = self.input_name.text()
            course: str = self.course_name.currentText()
            # course = self.course_name.itemText(self.cours_name.currentIndex())
            phone: int = int(self.input_phone.text())

            connection = connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            connection.execute(
                "INSERT INTO students (name, course, mobile) VALUES (?,?,?)", (name, course, phone))

            connection.commit()

            # Clear inputs
            self.input_name.setText("")
            self.input_phone.setText("")
            self.course_name.clear()
            self.course_name.setPlaceholderText("Select Course")
            self.course_name.addItems(['Math', 'Physics', 'Chemistry',
                                       'Biology', 'History', 'Science'])

            # FIXME had metaclass conflict when used @abstractmethod for def load_data() function
            # OR use main_window.load_data()
            self.success = True

        except sqlite3.Error as e:
            self.success = False
            print(e)
        finally:
            cursor.close()
            connection.close()

    def cancel(self) -> None:
        """
        This function is triggered when the cancel button is clicked. It closes the window.
            None
        """
        self.close()


class SearchDialog(QDialog):
    '''
    The SearchDialog class is used to search for a student record in the database. It contains several elements, such as labels, inputs, and buttons.

    The init method sets the window title, size, and creates a vertical layout for the elements. It also creates five labels for name, course, and phone, and five inputs for name, phone, course, and ID.

    Two buttons are created: Submit, Cancel. The Submit button is used to search for the data, while the Cancel button closes the window.

    The submit method is used to search for the data in the database. It first tries to search for the data, and if it fails, it displays an error message.

    Attributes:
    student_name (str): The name of the selected student record.
    student_course (str): The course of the selected student record.
    student_phone (int): The phone number of the selected student record.

    Methods:
    submit(self) -> None: This function is used to search for the data in the database.
    cancel(self) -> None: This function is used to close the window.

    '''

    def __init__(self) -> None:
        super().__init__()
        self.success: bool = False
        self.data: list[tuple] = []
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(280)

        # CREATE LAYOUT
        layout = QVBoxLayout()
        self.setLayout(layout)

        # CREATE LABELS
        self.label_name = QLabel("Name:")
        self.label_course = QLabel("Course:")
        self.label_phone = QLabel("Phone:")

        # CREATE INPUTS
        self.input_name = QLineEdit()
        self.input_phone = QLineEdit()

        self.input_name.setPlaceholderText("Student name")
        self.input_phone.setPlaceholderText("Studen phone number")

        # CREATE DROP DOWN MENU
        self.course_name = QComboBox()
        self.course_name.setPlaceholderText("Select Course")
        courses: list[str] = ['Math', 'Physics', 'Chemistry',
                              'Biology', 'History', 'Science']
        self.course_name.addItems(courses)

        # CREATE BUTTONS
        self.button_ok = QPushButton("Submit")
        self.button_cancel = QPushButton("Cancel")
        self.button_ok.clicked.connect(self.submit)
        self.button_cancel.clicked.connect(self.cancel)

        # ADD INPUTS TO LAYOUT
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(self.label_course)
        layout.addWidget(self.course_name)
        layout.addWidget(self.label_phone)
        layout.addWidget(self.input_phone)

        layout.addStretch()  # to push buttons down
        layout.addWidget(self.button_ok)
        layout.addWidget(self.button_cancel)

    def cancel(self) -> None:
        """
        This function is triggered when the cancel button is clicked. It closes the window.
        """
        self.close()

    def submit(self) -> None:
        """
        This function is used to search a new student record into the database.
        """
        try:
            name: Optional[str] = self.input_name.text() or None
            course: Optional[str] = self.course_name.currentText() or None
            phone: Optional[str] = self.input_phone.text() or None

            connection = connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            sql: str = f"SELECT * FROM students WHERE"
            params: list = []

            if name is not None:
                sql += " name=? AND"
                params.append(name)
            if course is not None:
                sql += " course=? AND"
                params.append(course)
            if phone is not None:
                sql += " mobile=? AND"
                params.append(int(phone))

            cursor.execute(
                sql[0:-3], (params))
            self.data = cursor.fetchall()

        except sqlite3.Error as e:
            self.success = False
            print(e)
        else:
            self.success = True
        finally:
            cursor.close()
            connection.close()


class EditDialog(QDialog):
    '''
    The EditDialog class is used to edit a student record in the database. It contains several elements, such as labels, inputs, and buttons.

    The init method sets the window title, size, and creates a vertical layout for the elements. It also gets the current row index and values from the table widget.

    Two buttons are created: Update, Cancel. The Update button is used to update the record, while the Cancel button closes the window.

    The submit method is used to update the record in the database. It first tries to update the record, and if it fails, it displays an error message.

    Attributes:
    student_id (int): The ID of the selected student record.
    student_name (str): The name of the selected student record.
    student_course (str): The course of the selected student record.
    student_phone (int): The phone number of the selected student record.

    Methods:
    submit(self) -> None: This function is used to update the record in the database.
    cancel(self) -> None: This function is used to close the window.
    '''

    def __init__(self) -> None:
        super().__init__()
        self.success: bool = False
        self.data: list[tuple] = []
        self.setWindowTitle("Edit Student Record")
        self.setFixedWidth(300)
        self.setFixedHeight(280)

        # CREATE LAYOUT
        layout = QVBoxLayout()
        self.setLayout(layout)

        # GET CURRENT ROW INDEX AND VALUES
        index = main_window.table.currentRow()
        # Row index and column index
        self.student_id: str = main_window.table.item(index, 0).text()
        student_name: str = main_window.table.item(index, 1).text()
        student_course: str = main_window.table.item(index, 2).text()
        student_phone: str = main_window.table.item(index, 3).text()

        # CREATE LABELS
        self.label_name = QLabel("Name:")
        self.label_course = QLabel("Course:")
        self.label_phone = QLabel("Phone:")

        # CREATE INPUTS
        self.input_name = QLineEdit(student_name)
        self.input_phone = QLineEdit(student_phone)

        self.input_name.setPlaceholderText("Student name")
        self.input_phone.setPlaceholderText("Studen phone number")

        # CREATE DROP DOWN MENU
        self.course_name = QComboBox()
        self.course_name.setPlaceholderText("Select Course")
        courses = ['Math', 'Physics', 'Chemistry',
                   'Biology', 'History', 'Science']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(student_course)

        # CREATE BUTTONS
        self.button_ok = QPushButton("Update")
        self.button_cancel = QPushButton("Cancel")
        self.button_ok.clicked.connect(self.submit)
        self.button_cancel.clicked.connect(self.cancel)

        # ADD INPUTS TO LAYOUT
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(self.label_course)
        layout.addWidget(self.course_name)
        layout.addWidget(self.label_phone)
        layout.addWidget(self.input_phone)

        layout.addStretch()  # to push buttons down
        layout.addWidget(self.button_ok)
        layout.addWidget(self.button_cancel)

    def cancel(self) -> None:
        """
        This function is triggered when the cancel button is clicked. It closes the window.
        """
        self.close()

    def submit(self) -> None:
        """
        This function is used to update a student record in the database.
        """
        try:
            name: Optional[str] = self.input_name.text() or None
            course: Optional[str] = self.course_name.currentText() or None
            phone: Optional[int] = int(self.input_phone.text()) or None

            connection = connection = DatabaseConnection().connect()

            cursor = connection.cursor()

            cursor.execute(
                "UPDATE students SET name=?, course=?, mobile=? WHERE id=?", (name, course, phone, self.student_id))

            connection.commit()

        except sqlite3.Error as e:
            self.success = False
            print(e)
        else:
            self.success = True
        finally:
            cursor.close()
            connection.close()
            self.close()


class DeleteDialog(QDialog):
    """
    This class is used to delete a student record from the database. 

    Attributes:
    student_id (int): The ID of the selected student record.
    student_name (str): The name of the selected student record.

    Methods:
    cancel(self) -> None: This function is triggered when the cancel button is clicked. It closes the window.
    submit(self) -> None: This function is used to delete a student record from the database. It opens the warning dialog box.
    delete(self) -> None: This function is used to delete a student record from the database.
    """

    def __init__(self) -> None:
        super().__init__()
        self.success: bool = False
        self.data: list[tuple] = []
        self.setWindowTitle("Delete Student Record")
        self.setFixedWidth(350)
        self.setFixedHeight(200)

        # CREATE LAYOUT
        layout = QVBoxLayout()
        self.setLayout(layout)

        # GET CURRENT ROW INDEX AND VALUES
        index: int = main_window.table.currentRow()

        # Row index and column index
        self.student_id: str = main_window.table.item(index, 0).text()
        student_name: str = main_window.table.item(index, 1).text()

        # CREATE LABELS
        self.label_question = QLabel(
            "Are you sure you want to delete this student?")
        self.label_name = QLabel(student_name)
        self.label_name.setStyleSheet("font-size: 12px; font-weight: bold;")

        # CREATE BUTTONS
        self.button_ok = QPushButton("Delete")
        self.button_ok.setStyleSheet(
            "font-weight: bold;")

        # self.button_ok.setFixedSize(QSize(100, 30))
        # self.button_ok.setFixedSize(100, 30)

        self.button_cancel = QPushButton("Cancel")
        self.button_ok.clicked.connect(self.submit)
        self.button_cancel.clicked.connect(self.cancel)

        # ADD INPUTS TO LAYOUT
        layout.addWidget(self.label_question)
        layout.addWidget(self.label_name)

        layout.addStretch()  # to push buttons down
        layout.addWidget(self.button_ok)
        layout.addWidget(self.button_cancel)

    def cancel(self) -> None:
        """
        This function is triggered when the cancel button is clicked. It closes the window.
        """
        self.close()

    def submit(self) -> None:
        """
        This function is used to delete a student record in the database, it opens the warning dialog box.
        """
        button = QMessageBox.critical(
            self,
            "Stop!",
            "Do you want to proceed with the deletetion?",
            buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            defaultButton=QMessageBox.StandardButton.Cancel,
        )

        if button == QMessageBox.StandardButton.Ok:
            self.delete()
            confirmation_widget = QMessageBox()
            confirmation_widget.setText(
                'The record has been deleted successfully.')
            confirmation_widget.exec()
        else:
            self.close()

    def delete(self) -> None:
        """
        This function is used to delete a student record from the database.
        """
        try:
            connection = connection = DatabaseConnection().connect()

            cursor = connection.cursor()

            cursor.execute(
                f"DELETE FROM students WHERE id={self.student_id}")

            connection.commit()

        except sqlite3.Error as e:
            self.success = False
            print(e)
        else:
            self.success = True
        finally:
            cursor.close()
            connection.close()
            self.close()


class AboutDialog(QDialog):
    """
    This class is used to create the about dialog box. It contains a text box that displays information about the application.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("About the program")
        self.setMinimumSize(600, 320)
        layout = QVBoxLayout()
        self.setLayout(layout)
        text: str = "<h2 style='letter-spacing:1.5px'>About this application</h2> \
        <p style='font-size:16px'>The purpose of this application was to explore api of PyQt6.</p> \
        <p style='font-size:16px'>This is a simple GUI application that uses SQL to manage a database of student records. The application has several features, including adding, editing, and deleting records. \
        It also allows you to search for a specific record using various criteria, such as name, course, and phone number.</p> \
        <p style='font-size:16px'>The application is built using PyQt6, a Python library for building GUI applications. The code is well-structured and follows best practices in software development, including using classes and functions to organize the code.</p>"
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setHtml(text)
        self.button_ok = QPushButton("OK")
        self.button_ok.clicked.connect(self.close)

        self.layout().addWidget(self.text_box)
        self.layout().addWidget(self.button_ok)


# Standurd setup
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
