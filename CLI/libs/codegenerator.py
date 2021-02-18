import json
from jinja2 import FileSystemLoader, Environment
from libs.database import Database

class CodeGenerator():
    """ CodeGenerator Class """
    def __init__(self, cmd_name:str, path):
        self.cmd_name = cmd_name

        # Jinja2 stuff
        self.file_loader = FileSystemLoader('templates')
        self.env = Environment(loader = self.file_loader)
        self.template = None

        # Database stuff
        self.database = Database(path)

    def generate_code(self):
        data = self.database.get_commands_where_cmd_name(self.cmd_name)
        
        # Message Variables
    
        cmd_name = data[0][0]
        cmd_type = data[0][1]
        title = self.none_checker(data[0][2])
        reply = self.none_checker(data[0][3])
        footer = self.none_checker(data[0][4])
        color = data[0][5]
        private = data[0][6]
        
        if cmd_type == "SIMPLE":
            if private == False:
                self.template = self.env.get_template("simple.txt")
                output = self.template.render(cmd_name = self.cmd_name, reply = reply)
                # Saving to database
                self.database.insert_update_output(cmd_name, output)

            elif private == True:
                self.template = self.env.get_template("simple_private.txt")
                output = self.template.render(cmd_name = self.cmd_name, reply = reply)
                # Saving to database
                self.database.insert_update_output(cmd_name, output)
                
        elif cmd_type == "EMBED":
            if private == False:
                self.template = self.env.get_template("embed.txt")
                output = self.template.render(cmd_name = self.cmd_name, title = title, reply = reply,
                                         color = color, footer = footer)
                # Saving to database
                self.database.insert_update_output(cmd_name, output)

            elif private == True:
                self.template = self.env.get_template("embed_private.txt")
                output = self.template.render(cmd_name = self.cmd_name, title = title, reply = reply,
                                         color = color, footer = footer)
                # Saving to database
                self.database.insert_update_output(cmd_name, output)

    def none_checker(self, word):
        if word != None:
            word = self.user_variable_converter(word)
        return word

              
    def user_variable_converter(self, word):
        # The [user] variable
        if "[user]" in word:
            word = word.replace("[user]", "{ctx.author.mention}")
        if "[user.id]" in word:
            word = word.replace("[user.id]", "{ctx.author.id}")
        if "[user.name]" in word:
            word = word.replace("[user.name]", "{ctx.author.display_name}")
        if "[user.discriminator]" in word:
            word = word.replace("[user.discriminator]", "{ctx.author.discriminator}")
        if "[user.avatar_url]" in word:
            word = word.replace("[user.avatar_url]", "{ctx.author.avatar_url}")

        # The [server] variable
        if "[server]" in word:
            word = word.replace("[server]", "{ctx.guild}")
        if "[server.id]" in word:
            word = word.replace("[server.id]", "{ctx.guild.id}")
        if "[server.icon_url]" in word:
            word = word.replace("[server.icon_url]", "{ctx.guild.icon_url}")
        if "[server.owner]" in word:
            word = word.replace("[server.owner]", "{ctx.guild.owner}")
        if "[server.owner_id]" in word:
            word = word.replace("[server.owner_id]", "{ctx.guild.owner_id}")
        if "[server.region]" in word:
            word = word.replace("[server.region]", "{ctx.guild.region}")
        if "[server.member_count]" in word:
            word = word.replace("[server.member_count]", "{ctx.guild.member_count}")

        # The Channel Variable
        if "[channel]" in word:
            word = word.replace("[channel]", "{ctx.channel}")
        if "[channel.name]" in word:
            word = word.replace("[channel.name]", "{ctx.channel.name}")
        if "[channel.id]" in word:
            word = word.replace("[channel.id]", "{ctx.channel.id}")

        return word


    def create_bot_file(self, prefix, output, token, path):
        self.template = self.env.get_template('bot.txt')
        result = self.template.render(prefix = prefix, output = output, token = token)

        f = open(f"{path}\\bot.py", "w")
        f.write(result)
        f.close()





    
