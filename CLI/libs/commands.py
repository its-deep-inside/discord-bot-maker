import sqlite3, json
from libs.database import Database
from libs.codegenerator import CodeGenerator

class EmbedMessage():
    """ Embed Message Class """
    def __init__(self, cmd_name:str, title:str, reply:str, footer:str, color:str, private:bool, path):
        # Creating Self Variables
        self.cmd_name = cmd_name
        self.cmd_type = "EMBED"
        self.title = title
        self.reply = reply
        self.footer = footer
        self.color = color
        self.private = private
        self.path = f"{path}\database.db"

        self.database = Database(self.path)
        self.add_to_database()

        
    def add_to_database(self):
        self.database.insert_update_commands(self.cmd_name, self.cmd_type, self.title,
                                             self.reply, self.footer, self.color,
                                             self.private)

        self.codegen = CodeGenerator(self.cmd_name, self.path)
        self.codegen.generate_code()

class SimpleMessage():
    """ Simple Message Class """
    def __init__(self, cmd_name:str, reply:str, private:bool, path):
        # Creating Self Variables
        self.cmd_name = cmd_name
        self.cmd_type = "SIMPLE"
        self.title = None
        self.reply = reply
        self.footer = None
        self.color = None
        self.private = private
        self.path = f"{path}\database.db"

        self.database = Database(self.path)
        self.add_to_database()

    def add_to_database(self):
        self.database.insert_update_commands(self.cmd_name, self.cmd_type, self.title,
                                            self.reply, self.footer, self.color,
                                             self.private)

        self.codegen = CodeGenerator(self.cmd_name, self.path)
        self.codegen.generate_code()






        
