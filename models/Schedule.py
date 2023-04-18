#!/usr/bin/python3
from sqlalchemy import false
import models
from models.baseModel import User, Base
from datetime import date, datetime
from models.baseModel import user_id

class Create_Schedule(User):
    """ 
        Class Create, updates and delete a new instance of the User class
    """
    # defines datetime attritributes 
    now_T = datetime.now()
    now = datetime(now_T.year, now_T.month, now_T.day, now_T.hour,
                   now_T.minute, 0)
    user = None
    # init method stores the data queried from the database
    def __init__(self, my_id):
        self.my_id = my_id
        self.__data = models.storage.view(self.my_id)

    """
        class method creates a new instance of the User class and
        stores it in the database
    """
    def Create(self, **kwargs):
        day = kwargs.get('Day')
        my_course = kwargs.get('Course')
        my_topic = kwargs.get('Topic')
        reminder = kwargs.get('Reminder')
        my_day = datetime.strptime(day, "%Y-%m-%d").date()
        my_reminder = datetime.strptime(reminder, "%H:%M:%S").time()
        if self.my_id is None:
            return f"user not found"
        else:
            self.user = User(
                                Days = my_day,
                                user_ID = self.my_id,
                                Course = my_course,
                                Topic = my_topic,
                                Reminder = my_reminder,
                                Target = False,
                                Average = None,
                                Created_at = self.now,
                                Updated_at = None
                            )

           # saves newly created instance of the User class and commits to database 
    def Save(self):
        """
            class method saves the newly created class instance to the database
        """
        models.storage.new(self.user)
        models.storage.save()
        models.storage.close()
        return True
          
     # deletes an instance of the User class and removes data from database
    def Delete(self, my_id, deldata=None):
        """
            Deletes and modifies data queried from the database by object ID
        """
        deldata = models.storage.view(my_id)[0].get(my_id)
        deldata = deldata.schedules.all()
        if deldata is None:
            return False
        else:
            for data in deldata:
                models.storage.delete(data)
                models.storage.save()
            models.storage.close()
            return True


    def View(self, my_id, choice=None, table=None):
        """
            class method queries the database and returns a dictionary value
            based on the specified query method
        """
        if table is None:
            new = models.storage.access(my_id, 'id', user_id)
            tasks = new.schedules.all()
        else:
            tasks = None
            new = models.storage.access(my_id, 'id', user_id)
            file = {
                    "Python" : new.auto_schedules.all(),
                    "Javascript" : new.JScourse.all(),
                    "React" : new.Reactcourse.all(),
                    "C" : new.C_course.all()
                }
            if table in file:
                tasks = file.get(table)

        new_dict = {}
        new_dict_2 = {}
        short_date = self.now.strftime("%Y-%m-%d")
        if tasks is None:
            return f"data empty"

        for task in tasks:
                new_dict[task.id] = {"Date":task.Days,
                             "Course": task.Course,
                             "Topic": task.Topic,
                             "Target": task.Target,
                             "Average":task.Average,
                             "Reminder": task.Reminder, 
                             "Created":task.Created_at
                        }
        if choice is None:
            for k, v in new_dict.items():
                return (new_dict)
        elif choice.lower() == "upcoming":
            for k, v in new_dict.items():
                if v["Date"] > short_date:
                    new_dict_2[k] = v
        elif choice.lower() == "daily":
            for k, v in new_dict.items():
                if v["Date"] == short_date:
                    new_dict_2[k] = v
        elif choice.lower() == "missed":
            for k, v in new_dict.items():
                if v["Date"] < short_date and v['Target'] is False:
                    new_dict_2[k] = v
        else:
            raise ValueError(f"view either [upcoming, daily, missed]")
        models.storage.close()
        return new_dict_2

    def Target(self, my_id, course):
        data = self.__data[0].get(my_id)
        file = {
                "Python" : data.auto_schedules.all(),
                "Javascript" : data.JScourse.all(),
                "React" : data.Reactcourse.all(),
                "C" : data.C_course.all()
            }
        if not file.get(course):
            return (0, file)
        else:
            python_Target = [x.Target for x in file.get(course)]
            python_Target = [int(b) for b in python_Target]
            python_mean_Target = sum(python_Target) / len(python_Target)
            python_mean_Target = round(python_mean_Target, 2)
            return (python_mean_Target, file)
    
    def DeleteAll(self, my_id, course):
        course_file = []
        for idx, file  in enumerate(course):
            if idx > 0:
                break
            course_file.append(self.Target(my_id, file)[1])

        course_file = course_file[0]
        status = False
        while any(course_file.values()):
            for _, value in course_file.items():
                if value == []:
                    continue
                for val in value:
                    models.storage.delete(val)
                    models.storage.save()
                    value.remove(val)
                    status = True
            models.storage.close()
        return status



