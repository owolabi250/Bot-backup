#import models
import pytest
import models
from models import storage
from models.baseModel import User, Base
from datetime import date, datetime
from models.Schedule import Create_Schedule
from _pytest.monkeypatch import MonkeyPatch


class BaseTest:
    def setup(self, monkeypatch: MonkeyPatch):
        self.monkeypatch = monkeypatch

class TestCreateSchedule(BaseTest):
    def setup_method(self):
        self.schedule = Create_Schedule()
        self.my_day = "2022-01-01"
        self.my_course = "Math"
        self.my_topic = "Algebra"
        self.my_reminder = "12:00:00"
        self.schedule.Create(self.my_day, self.my_course, self.my_topic,
                             self.my_reminder)
  
    @pytest.fixture
    def Addup(self):
        self.schedule = Create_Schedule()
        self.schedule.Create("2022-12-12", "Math", "Algebra", "10:00:00")
        return self.schedule

    def test_create(self):
        assert isinstance(self.schedule.user, User)
        assert self.schedule.user.Days == date(2022, 1, 1)
        assert self.schedule.user.Course == "Math"
        assert self.schedule.user.Topic == "Algebra"
        assert self.schedule.user.Reminder == datetime.strptime(
                                self.my_reminder,"%H:%M:%S").time()
        assert self.schedule.user.Target == False
        assert self.schedule.user.Average == None
        assert self.schedule.user.Created_at == self.schedule.now
        assert self.schedule.user.Updated_at == None

    def test_delete_schedule(self, monkeypatch):
        monkeypatch.setattr(models.storage, 'view', lambda: {'1': User(Days=date(2022, 1, 1), Course='Math',
                            Topic='Algebra', Reminder=datetime.strptime(self.my_reminder, "%H:%M:%S").time(),
                            Target=False, Average=None, Created_at=datetime.now(), Updated_at=None)})
        monkeypatch.setattr(models.storage, 'delete', lambda x: None)
        monkeypatch.setattr(models.storage, 'save', lambda: None)
        monkeypatch.setattr('builtins.input', lambda x: 1)
        schedule = Create_Schedule()
        schedule.Delete('1')
        assert schedule.user is None
    def test_view_schedule(self, monkeypatch):
        monkeypatch.setattr(models.storage, 'view', lambda: {'1': User(Days=date(2022, 1, 1), Course='Math', Topic='Algebra',
                            Reminder=datetime.strptime(self.my_reminder, "%H:%M:%S").time(), 
                            Target=False, Average=None, Created_at=datetime.now(), Updated_at=None)})
        schedule = Create_Schedule()
        schedule.Create(self.my_day, self.my_course, self.my_topic, self.my_reminder)
        schedule.View()
        assert schedule.user is not None

    def test_update_course(self, Addup):
        Addup.Update(1, "Physics", 1)
        assert Create_Schedule.__data[1].Course == "Physics"

