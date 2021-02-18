import argparse, sqlite3, sys, os
from libs.commands import EmbedMessage, SimpleMessage
from libs.database import Database
from libs.codegenerator import CodeGenerator

conn = sqlite3.connect('default.db')
cursor = conn.cursor()

# create a tabel which will store projects naem and path
def create_default_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS projects(
                    project_name text PRIMARY KEY,
                    project_path text
                    )""")
    conn.commit()


# Insert Data in the table we created
def insert_data(project_name, project_path):
    
    # get all data from projects table where
    cursor.execute("SELECT * FROM projects WHERE project_name = ? OR project_path = ?" , (project_name, project_path,))
    data = cursor.fetchall()
    # check if project_name and path exists
    if data == []:
        cursor.execute("INSERT INTO projects VALUES(?, ?)", (project_name, project_path,))
        conn.commit()
    else:
        # throw custom error and exit
        sys.exit("Name or Path Already exists")

# Get Data Where Project Name is project_name
def get_data_where(project_name):
    cursor.execute("SELECT * FROM projects WHERE project_name = ?", (project_name,))
    return cursor.fetchone()

# Create New Project
def create_new_project(args):
    if os.path.exists(args.npth):
        if os.listdir(args.npth) == []:
            insert_data(args.np, args.npth)
        else:
            sys.exit("Please provide an empty path.")
    else:
            sys.exit("Path not exists.")

# Create Commands
def create_commands(args):
    if args.type.upper() == "EMBED":
        path = get_data_where(args.p)[1]
        new_cmd = EmbedMessage(args.name, args.title, args.reply,
                               args.footer, f"0x{args.color}", args.private, path)
        print(f"Command {args.name} Added.")
        
    elif args.type.upper() == "SIMPLE":
        path = get_data_where(args.p)[1]
        new_cmd = SimpleMessage(args.name, args.reply, args.private, path)
        print(f"Command {args.name} Added.")

    else:
        sys.exit(f"There is no type called {args.type}. Try using '-h'")

# Check wether private is tru or false
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
      
# Main Function
if __name__ == '__main__':
    # DATABASE STUFF
    create_default_table()

    # COMMANDS STUFF
    parser = argparse.ArgumentParser()

    # New Project Commands
    parser.add_argument('-np', '--new_project', type=str, dest="np" ,help="Used to create new Project. ['-npth' is required].")
    parser.add_argument('-npth', '--path', type=str, dest="npth" ,help="New Project's Path. [Use with '-np'].")

    # Old Projct Commands
    parser.add_argument('-p', '--project', type=str, dest="p" , help="Used to tell program which project to edit. example: -p Docs Bot")
    parser.add_argument('-type', type=str, dest="type" , help="Type of message.\nMain two types are:\n1) SIMPLE\n2) EMBED.")
    parser.add_argument('-n', '--name', type=str, dest="name" , help="name of command.")
    parser.add_argument('-t', '--title', type=str, dest="title" , help="title of embed message.")
    parser.add_argument('-r', '--reply', type=str, dest="reply" , help="reply for simple message and description for embed message.")
    parser.add_argument('-foot', '--footer', type=str, dest="footer" , help="footer of embed.")
    parser.add_argument('-c', '--color', type=str, dest="color" , help="color of embed.")
    parser.add_argument('-prv', '--private', type=str2bool, dest="private" , help="true of send message in DM and false if send in channel.")
    parser.add_argument('--commands', dest="commands", action='store_true', help="all added commands of a project. also use '-p'.")
    parser.add_argument('--finish', dest="finish", action="store_true", help="finish project [REQUIRED: '-prefix', '-token'].")
    parser.add_argument('-prefix', dest="prefix",type=str, help="prefix of bot.")
    parser.add_argument('-token', dest="token",type=str, help="token of your bot.")
    parser.add_argument('-delp', '--delete_project', dest="delete_project",type=str, help="delete project")
    parser.add_argument('-delc', '--delete_command', dest="delete_command",type=str, help="delete command")
    parser.add_argument('--projects', dest="projects", action="store_true", help="all projects")
    

    # get input from parser
    args = parser.parse_args()
    # check for current project or new project
    if args.p == None and args.np != None:
        create_new_project(args)
    elif args.p != None and args.p.strip() != "" and args.type != None:
        create_commands(args)

    # check for if --commands used
    if args.commands:
        try:
            path = f"{get_data_where(args.p)[1]}\database.db"
            x = Database(path)
            data = x.get_all_commands()
            for x in data:
                print(x[0])
        except sqlite3.OperationalError:
            sys.exit(f"No project called {args.p}")

    # check if --finish used
    if args.finish:
        path = f"{get_data_where(args.p)[1]}\database.db"
        db = Database(path)
        data = db.get_all_output()
        output = []
        for x in data:
            output.append(x[1])

        # generate code
        code_gen = CodeGenerator('test', path)
        code_gen.create_bot_file(args.prefix, output, args.token, get_data_where(args.p)[1])

    # delete project
    if args.delete_project != None and args.delete_project.strip() != "":
        cursor.execute("DELETE FROM projects WHERE project_name = ?", (args.delete_project,))
        conn.commit()
        print("Projected Removed")

    # delete command
    if args.delete_command != None and args.delete_command.strip() != "":
        path = f"{get_data_where(args.p)[1]}\database.db"
        db = Database(path)
        db.delete_commands(args.delc)
        print("Command Deleted")

    # Get all projects
    if args.projects:
        cursor.execute("SELECT * FROM projects")
        data = cursor.fetchall()
        if data == []:
            print("No projects.")
        else:
            for x in data:
                print(x[0])

    
    
    
