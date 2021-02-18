import sqlite3

class Database():
    """ Database Editing Class """
    def __init__(self, path):
        # Creating self variables
        self.path = path
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.create_commands_table()
        self.create_output_table()

    # -----------------COMMANDS STUFF--------------------#
    def create_commands_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS commands(
                            cmd_name text PRIMARY KEY,
                            cmd_type text,
                            title text,
                            reply text,
                            footer text,
                            color text,
                            private boolean
                            )""")

        self.conn.commit()

    def insert_update_commands(self, cmd_name, cmd_type, title, reply, footer, color, private):
        self.cursor.execute("""INSERT INTO commands VALUES (?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT(cmd_name) DO UPDATE SET cmd_type=?, title=?, reply=?, footer=?, color=?, private=?""",
                            (cmd_name, cmd_type, title, reply, footer, color, private,
                             cmd_type, title, reply, footer, color, private,)
                            )

        self.conn.commit()

    def get_all_commands(self):
        self.cursor.execute("SELECT * FROM commands")
        return self.cursor.fetchall()

    def get_commands_where_cmd_name(self, cmd_name):
        self.cursor.execute("SELECT * FROM commands WHERE cmd_name = ?", (cmd_name,))
        return self.cursor.fetchall()

    # -----------------OUTPUT STUFF------------------#
    def create_output_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS output(
                            cmd_name text PRIMARY KEY,
                            cmd_output text
                            )""")
        self.conn.commit()

    def insert_update_output(self, cmd_name, cmd_output):
        self.cursor.execute("INSERT INTO output VALUES (?, ?) ON CONFLICT(cmd_name) DO UPDATE SET cmd_output =?",
                            (cmd_name, cmd_output, cmd_output))
        self.conn.commit()

    def get_all_output(self):
        self.cursor.execute("SELECT * FROM output")
        return self.cursor.fetchall()
    
    def get_output_where_cmd_name(self, cmd_name):
        self.cursor.execute("SELECT * FROM output WHERE cmd_name = ?", (cmd_name,))
        return self.cursor.fetchall()


    #---------------------Delete from both table----------------#
    def delete_commands(self, cmd_name):
        self.cursor.execute("DELETE FROM commands WHERE cmd_name = ?", (cmd_name,))
        self.cursor.execute("DELETE FROM output WHERE cmd_name = ?", (cmd_name,))
        self.conn.commit()


