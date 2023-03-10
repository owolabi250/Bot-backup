#!/usr/bin/python3
from sqlalchemy import false
import models
from models.baseModel import User, Base
from datetime import date, datetime

class Create_Schedule(User):
    """ 
        Class Create, updates and delete a new instance of the User class
    """
    # defines datetime attritributes 
    now_T = datetime.now()
    now = datetime(now_T.year, now_T.month, now_T.day, now_T.hour,
                   now_T.minute, 0)
    user = None
    
    def __init__(self):
        self.__data = models.storage.view()
        pass
    # Creates an instance of the User class

    def Create(self, **kwargs):
        day = kwargs.get('Day')
        my_course = kwargs.get('Course')
        my_topic = kwargs.get('Topic')
        reminder = kwargs.get('Reminder')
        my_day = datetime.strptime(day, "%Y-%m-%d").date()
        my_reminder = datetime.strptime(reminder, "%H:%M:%S").time()
        self.user = User(
                            Days = my_day,
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
        deldata = self.__data.get(my_id, None)
        if deldata is None:
            print("data not found confirm data ID")
        else:
            models.storage.delete(deldata)
            models.storage.save()
            models.storage.close()


    def View(self, choice=None):
        """
            class method queries the database and returns a dictionary value
            based on the specified query method
        """
        new_dict = {}
        new_dict_2 = {}
        short_date = self.now.strftime("%Y-%m-%d")
        if self.__data is None:
            print("empty")
        for key, V in self.__data.items():
                new_dict[key] = {"Date":V.Days,
                             "Course": V.Course,
                             "Topic": V.Topic,
                             "Target": V.Target,
                             "Average":V.Average,
                             "Reminder": V.Reminder, 
                             "Created":V.Created_at
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
                if v["Date"] < short_date and v['Target'] == False:
                    new_dict_2[k] = v
        else:
            raise ValueError(f"view either [upcoming, daily, missed]")
        models.storage.close()
        return new_dict_2


    def Update(self, my_id, arg, option=None):
        """
            Update a data in the database based on the object ID, specified 
            parameters to update and column to modify
        """
        if self.__data and arg is not None:
            if  option == 0:
                self.__data[my_id].Course  = arg
                self.__data[my_id].Updated_at = self.now
                print("Course updated")
            elif option == 1:
                self.__data[my_id].Topic = arg
                self.__data[my_id].Updated_at = self.now
                print("Topic updated")
            elif option == 2:
                self.__data[my_id].Reminder = arg
                self.__data[my_id].Updated_at = self.now
                print("Reminder updated")
            elif option == 4:
                self.__data[my_id].Target = 1
                self.__data[my_id].Average = arg
                self.__data[my_id].Updated_at = self.now
                models.storage.save()
            else:
                print("data empty")
        models.storage.save()

   

    def bm_update(self, my_id, attr_dict=None):
        """
            updates the basemodel and sets the correct attributes
        """
        IGNORE = [
              'Target', 'Days', 'Created_at' ]
        if attr_dict:
            updated_dict = {
                  k: v for k, v in attr_dict.items() if k not in IGNORE
              }
            for key, value in updated_dict.items():
                if key == 'Topic':
                    self.__data[my_id].Topic = value
                elif key == 'Course':
                    self.__data[my_id].Course = value
                elif key == 'Reminder':
                    self.__data[my_id].Reminder = value
                else:
                    return {"error": "key not found"}
                self.__data[my_id].Updated_at = self.now
                models.storage.save()
                models.storage.close()
                return updated_dict
        else:
            return {"error": "empty dictionary"}
    
