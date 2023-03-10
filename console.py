#!/usr/bin/python3

# from numpy import empty
from sqlalchemy.util import WeakSequence
from models import graph
from models.Schedule import Create_Schedule
from models.Reminder import Reminder
from models.checker import Checker
from models.security import Login
from models.graph import Plot
import cmd
import platform
import models
import argparse
import threading
import time
import subprocess
import os

data = Create_Schedule()
def Parser(arg):
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(dest='choice', type=str, help='view', default=None, nargs='?')
        return parser.parse_args(arg.split())
    except ValueError as e:
        print(e)


class BOT(cmd.Cmd):
    intro = "*** Welcome to the BotSchedule Command line interface Type help or ? to view commands ***"
    prompt = "(Bot) "
    
    def emptyline(self):
        """do nothing upon recieving an emptyline """
        pass

    def do_clear(self, arg):
        os.system('clear' if os.name == 'posix' else 'cls')
        args = Parser(arg)
        if args.choice == 'clear':
            self.do_clear(args.choice)
        else:
            pass

    def do_Create(self, arg):
        """ to create a Schedule type of the following accordingly,
            Create [set day format %Y-%m-%d] [set course]
                   [set topic] [set reminder format %H:%M:%S].
        """
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument(dest='day', type=str, help='enter date')
            parser.add_argument(dest='course', type=str, help='add course')
            parser.add_argument(dest='topic', type=str, help='add topic')
            parser.add_argument(dest='reminder', type=str, help='set reminder')
            args = parser.parse_args(arg.split())
            dic = {
                    "Day" : args.day,
                    "Course" : args.course,
                    "Topic" : args.topic,
                    "Reminder" : args.reminder
                    }
            if len(arg) < 4:
                print("press [help Create]  for options")
            else:
                data.Create(**dic)
                print("Successful")
                data.Save()

        except Exception as e:
            print("some error occured press [help Create]  for options", e)
        except SystemExit:
            print("wrong input press [help Create] for guideline")


    def do_weather(self, arg):
        result = subprocess.run(['curl', 'wttr.in/lon'], stdout=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))

    def do_Delete(self, arg):
        """ to delete a schedule from the database input the data ID as follow,
            Delete [enter data id] """
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument(dest='my_id', type=int, help='enter Id to delete data from')
            args = parser.parse_args(arg.split())
            if len(arg) == 0 and args.my_id is None:
                print("press [help Delete] for options")
            else:
                data.Delete(args.my_id)
        except Exception as e:
            print("some error occured press [help Delete]  for options", e)
        except SystemExit:
            print("wrong input press [help Delete] for guidelines")

    def do_View(self, arg):
        """ to view schedule press View [option] 
            you can View missed, daily, upcoming or type view with no argument 
            to view all """
        try:
            args = Parser(arg)
            doc = data.View(args.choice)
            if len(doc) == 0:
                print("\nempty set")
            else:
                for key, value in doc.items():
                    print(f"{key} {value}\n")
        except Exception as e:
            print("some error occured", e)
        except SystemExit:
            print("wrong input press [help View] for guidelines")

    def do_Update(self, arg):
        """to update a schedule specify the data ID followed by the data to update
            Update [ID] [arg] [option] eg 0:Course, 1:Topic, 2:set new Reminder
        """
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument(dest='my_id', type=int, help='enter Id to delete data from')
            parser.add_argument(dest='my_arg', type=str, help='enter new details to update')
            parser.add_argument(dest='option', type=int, help='option')
            args = parser.parse_args(arg.split())
            if len(arg) < 3:
                print("type help Update for instructions")
            else:
                data.Update(args.my_id, args.my_arg, args.option)
        except Exception as e:
            print("some error occured", e)
        except SystemExit:
            print("wrong input press [help View] for guidelines")

	    
    def do_Reminder(self, arg):
        """ to view reminder enter the command Reminder
            which sends a reminder to your twilio account"""
        try:
            obj = Reminder()
            print("please wait ... ")
            print("Reminder set for {}".format(obj.reminder))
            thread = threading.Thread(target=obj.send_Reminder)
            thread.start()
            print("number of threads running {}".format(threading.active_count()))
        except SystemExit:
            print("some error occurred")
        except KeyboardInterrupt:
            print("process terminated")

    def do_AI(self, arg):
        """ the AI is a personal assistant that helps recommend resources to read
            alongsides answers questions regarding vast range of topic. to use,
            run the command AI [input question to ask] """
        try:
            bot = Checker()
            args = Parser(arg)
            opt = 0
            while opt == 0:
                if args.choice is not None:
                    args.choice = str(input("BOT$ How can i help you: "))
                    voice = bot.Help(args.choice)
                    print(f"{voice} \n")
                else:
                    print("here are your resources based on todays task \n")
                    voice = bot.Help()
                    print(f"{voice} \n")
                opt = int(input("do you have any other questions? press 1 to quit: "))
        except Exception as e:
            print("wrong input type", e)
        except SystemExit as s:
            print(s)

    def do_Chart(self, arg):
        """ to plot the graph of your performance run the command Plot on the
            commandline """
        try:
            graph = Plot()
            graph.Daily()
        except SystemExit as e:
            print(e)
	
    def do_quit(self, arg):
        """Quit command to exit the program"""
        end_time = time.time()
        total_time = end_time - start_time
        systm = platform.system()
        print("\nsystem information>>> login time: {:2f} sec Device: {}\n".
                format(total_time, systm))
        print("\n Goodbye \n")
        return True





if __name__ == '__main__':
    start_time = time.time()
    # passkey = Login()
    # if passkey.login() == True:
    BOT().cmdloop()
