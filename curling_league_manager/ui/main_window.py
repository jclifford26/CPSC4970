import os
import sys
import copy

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox

from curling_league_manager.league.league_database import LeagueDatabase
from curling_league_manager.league.league import League
from curling_league_manager.ui.league_editor import LeagueEditor

ui_path = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, QtBaseWindow = uic.loadUiType(os.path.join(ui_path, "main_window.ui"))


def alert(title, message):
    mb = QMessageBox(QMessageBox.Icon.Warning, title, message, QMessageBox.StandardButton.Ok)
    return mb.exec()


def action_quit_triggered():
    sys.exit(QtWidgets.QApplication(sys.argv).exec_())


class MainWindow(QtBaseWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.deleteLeagueBtn.clicked.connect(self.delete_league_btn_clicked)
        self.addLeagueBtn.clicked.connect(self.add_league_btn_clicked)
        self.editLeagueBtn.clicked.connect(self.edit_league_btn_clicked)
        self.actionLoad.triggered.connect(self.action_load_triggered)
        self.actionSave.triggered.connect(self.action_save_triggered)
        self.actionQuit.triggered.connect(action_quit_triggered)
        self.leagues = []
        self._db = LeagueDatabase()

    def delete_league_btn_clicked(self):
        league_to_remove = self.get_current_selected_league()
        if league_to_remove:
            self.leagues.remove(league_to_remove)
            self.update_ui()
        else:
            alert("League not Selected", "Please select a league to delete.")

    def add_league_btn_clicked(self):
        league_name = self.leagueLineEdit.text()
        if league_name:
            new_league = League(self._db.instance().next_oid(), league_name)
            self.leagues.append(new_league)
            self.update_ui()
            self.leagueLineEdit.clear()
        else:
            alert("Name not Entered", "Please enter a league name to add.")

    def edit_league_btn_clicked(self):
        league_to_edit = copy.deepcopy(self.get_current_selected_league())
        current_index = self.displayLeague.currentRow()
        if league_to_edit:
            edit_league_window = LeagueEditor(self._db, league_to_edit)
            edit_league_window.update_ui()
            if edit_league_window.exec_() == QDialog.Accepted:
                self.leagues.remove(league_to_edit)
                self.leagues.insert(current_index, edit_league_window.league)
                self.update_ui()
            else:
                self.update_ui()
        else:
            alert("League not Selected", "Please select a league to edit.")

    def action_load_triggered(self):
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(["All files (*.*)", "DAT (*.dat)"])
        dialog.selectNameFilter("DAT (*.dat)")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._db.instance().leagues = []
            self.leagues = []
            filepath = dialog.selectedFiles()[0]
            try:
                self._db.instance().load(filepath)
                self.leagues.extend(self._db.instance().leagues)
                self.update_ui()
            except Exception as e:
                alert("File Load Error", f"Error loading file: {e}")
        else:
            alert("File Load Cancelled", "Unable to load the specified file.")

    def action_save_triggered(self):
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(["All files (*.*)", "DAT (*.dat)"])
        dialog.selectNameFilter("DAT (*.dat)")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._db.instance().leagues = []
            filepath = dialog.selectedFiles()[0]
            try:
                self._db.instance().leagues.extend(self.leagues)
                self._db.instance().save(filepath)
                self.update_ui()
            except Exception as e:
                alert("File Save Error", f"Error saving file: {e}")
        else:
            alert("File Save Cancelled", "Unable to save the specified file.")

    def get_current_selected_league(self):
        if len(self.displayLeague.selectedItems()) > 0:
            selection_text = self.displayLeague.currentItem().text()
            league_name, _ = selection_text.split(':')
            for league in self.leagues:
                if league.name == league_name:
                    return league

    def update_ui(self):
        self.displayLeague.clear()
        for league in self.leagues:
            self.displayLeague.addItem(str(league))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
