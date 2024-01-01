# EXPLORING PyQt6 TO BUILD SIMPLE GUI

### Purpose
This app is basic and was built to simply explote the PyQt6 api.
Inspired by Ardit Sulce.

### Methods
The main.py file initializes the GUI and creates the main window for a student management system. It uses the PyQt6 library to create the GUI elements, such as buttons, labels, and text fields.

The main function creates a MainWindow object and sets its title, size, and central widget. It then creates a menu bar with three menus: File, Help, and Edit. The File menu contains an "Add Student" action, which opens the AddDialog when triggered. The Help menu contains an "About" action. The Edit menu contains 

an "Edit Student" action, which opens the EditDialog when triggered.

Two buttons are created: Add Student, Search Record. The Add Student button is used to add a new student record, the Search Record button is used to search for a student record.

A table widget is created to display the student records. The table contains four columns, ID, Name, Course, and Phone. The row headers are hidden to avoid extra indices.

The load_data method is used to load the data from the database into the table widget.

The cell_clicked function is triggered when a cell in the table is clicked. It adds two buttons to the status bar, "Edit Record" and "Delete Record", which allow the user to edit or delete the corresponding record in the table.

The edit_record function is triggered when the edit button in the status bar is clicked. It opens the EditDialog, which allows the user to edit the selected record in the table.

The delete_record function is triggered when the delete button in the status bar is clicked. It opens the DeleteDialog, which allows the user to delete the selected record in the table.

The insert method is used to insert a new student record into the database.

The search method is used to search for a student record in the database.

The about method is triggered when the about button is clicked. It opens the about dialog box.

### Screenshots
![Screenshot 2024-01-01 at 2 25 42 PM](https://github.com/LearnFL/proj-python-gui-student-management/assets/86169204/6aed145b-04b1-458c-b5ec-5b896b494277)
![Screenshot 2024-01-01 at 2 25 55 PM](https://github.com/LearnFL/proj-python-gui-student-management/assets/86169204/9423ece2-9abd-4c87-8b9b-0a9bdf7afb8e)
![Screenshot 2024-01-01 at 2 26 22 PM](https://github.com/LearnFL/proj-python-gui-student-management/assets/86169204/6658be8c-176b-4493-bf1a-2737a416eb6e)
![Screenshot 2024-01-01 at 2 26 51 PM](https://github.com/LearnFL/proj-python-gui-student-management/assets/86169204/1946b898-1503-4d26-9b73-6e108bfc8f56)
