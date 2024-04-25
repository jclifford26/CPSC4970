import os
import sys
import copy

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog

from curling_league_manager.league.league import League
from curling_league_manager.league.league_database import LeagueDatabase
from curling_league_manager.league.team import Team
from curling_league_manager.ui.team_editor import TeamEditor

ui_path = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, QtBaseWindow = uic.loadUiType(os.path.join(ui_path, "league_editor.ui"))


def alert(title, message):
    mb = QMessageBox(QMessageBox.Icon.Warning, title, message, QMessageBox.StandardButton.Ok)
    return mb.exec()


class LeagueEditor(QtBaseWindow, Ui_MainWindow):
    def __init__(self, database, league, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.deleteTeamBtn.clicked.connect(self.delete_team_btn_clicked)
        self.addTeamBtn.clicked.connect(self.add_team_btn_clicked)
        self.editTeamBtn.clicked.connect(self.edit_team_btn_clicked)
        self.importLeagueBtn.clicked.connect(self.import_league_clicked)
        self.exportLeagueBtn.clicked.connect(self.export_league_clicked)
        self.league = league
        self._db = database

    def delete_team_btn_clicked(self):
        team_to_remove = self.get_current_selected_team()
        if team_to_remove:
            self.league.remove_team(team_to_remove)
            self.update_ui()
        else:
            alert("Team not Selected", "Please select a team to delete.")

    def add_team_btn_clicked(self):
        team_name = self.teamLineEdit.text()
        if team_name:
            new_team = Team(self._db.instance().next_oid(), team_name)
            self.league.add_team(new_team)
            self.update_ui()
        else:
            alert("Name not Entered", "Please enter a team to add.")

    def edit_team_btn_clicked(self):
        team_to_edit = copy.deepcopy(self.get_current_selected_team())
        current_index = self.displayTeam.currentRow()
        if team_to_edit:
            edit_team_window = TeamEditor(self._db, team_to_edit)
            edit_team_window.update_ui()
            if edit_team_window.exec_() == QDialog.DialogCode.Accepted:
                self.league.teams.remove(team_to_edit)
                self.league.teams.insert(current_index, edit_team_window.team)
                self.update_ui()
            else:
                self.update_ui()
        else:
            alert("Team not Selected", "Please select a team to edit.")

    def export_league_clicked(self):
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(["All files (*.*)", "CSV (*.csv)"])
        dialog.selectNameFilter("CSV (*.csv)")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            filepath = dialog.selectedFiles()[0]
            self._db.instance().add_league(self.league)
            self._db.instance().export_league(self.league, filepath)
        else:
            alert("File Export Cancelled", "Unable to export the specified file.")

    def import_league_clicked(self):
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(["All files (*.*)", "CSV (*.csv)"])
        dialog.selectNameFilter("CSV (*.csv)")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            filepath = dialog.selectedFiles()[0]
            self._db.instance().import_league(self.league.name, filepath)
            self.league = self._db.instance().leagues[-1]
            self.update_ui()
        else:
            alert("File Import Cancelled", "Unable to import the specified file.")

    def get_current_selected_team(self):
        if len(self.displayTeam.selectedItems()) > 0:
            selection_text = self.displayTeam.currentItem().text()
            team_name, _ = selection_text.split(':')
            for team in self.league.teams:
                if team.name == team_name:
                    return team

    def update_ui(self):
        self.displayTeam.clear()
        self.teamLineEdit.clear()
        for team in self.league.teams:
            self.displayTeam.addItem(str(team))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueEditor(LeagueDatabase(), League(0, "Test League"))
    window.show()
    sys.exit(app.exec_())
