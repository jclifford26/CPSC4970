import os
import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from curling_league_manager.league.league_database import LeagueDatabase
from curling_league_manager.league.team import Team
from curling_league_manager.league.team_member import TeamMember

ui_path = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, QtBaseWindow = uic.loadUiType(os.path.join(ui_path, "team_editor.ui"))


def alert(title, message):
    mb = QMessageBox(QMessageBox.Icon.Warning, title, message, QMessageBox.StandardButton.Ok)
    return mb.exec()


class TeamEditor(QtBaseWindow, Ui_MainWindow):
    def __init__(self, database, team, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.deleteMemberBtn.clicked.connect(self.delete_member_btn_clicked)
        self.addMemberBtn.clicked.connect(self.add_member_btn_clicked)
        self.updateMemberBtn.clicked.connect(self.update_member_btn_clicked)
        self.displayMember.itemClicked.connect(self.item_clicked)
        self.team = team
        self._db = database

    def delete_member_btn_clicked(self):
        member_to_remove = self.get_current_selected_member()
        if member_to_remove:
            self.team.remove_member(member_to_remove)
            self.update_ui()
        else:
            alert("Member not Selected", "Please select a member to delete.")

    def add_member_btn_clicked(self):
        name = self.memberLineEdit.text()
        email = self.emailLineEdit.text()
        if name:
            new_member = TeamMember(self._db.instance().next_oid(), name, email)
            self.team.add_member(new_member)
            self.update_ui()
        else:
            alert("Name not Entered", "Please enter a name to add.")

    def update_member_btn_clicked(self):
        member_to_update = self.get_current_selected_member()
        if member_to_update:
            member_to_update.name = self.memberLineEdit.text()
            member_to_update.email = self.emailLineEdit.text()
            self.update_ui()
        else:
            alert("Member not Selected", "Please select a member to update.")

    def get_current_selected_member(self):
        if len(self.displayMember.selectedItems()) > 0:
            selection_text = self.displayMember.currentItem().text()
            name, email = selection_text.split('<')
            for member in self.team.members:
                if member.name == name and member.email == email[:-1]:
                    return member

    def item_clicked(self):
        member_selected = self.get_current_selected_member()
        self.memberLineEdit.setText(member_selected.name)
        self.emailLineEdit.setText(member_selected.email)

    def update_ui(self):
        self.displayMember.clear()
        self.memberLineEdit.clear()
        self.emailLineEdit.clear()
        for member in self.team.members:
            self.displayMember.addItem(str(member))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamEditor(LeagueDatabase(), Team(0, "Test Team"))
    window.show()
    sys.exit(app.exec_())
