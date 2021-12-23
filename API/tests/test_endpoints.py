from unittest import TestCase
from flask_restx import Resource
import random

import API.endpoints as ep
import db.data as db

HUGE_NUM = 10000000000000  # any big number will do!


def new_entity_name(entity_type):
    int_name = random.randint(0, HUGE_NUM)
    return f"new {entity_type}" + str(int_name)


class EndpointTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_app(self):
        testrun = ep.AppTest(Resource)
        ret = testrun.get()
        self.assertIsInstance(ret, dict)
        self.assertIn(ep.WORKING_MSG, ret)

    def test_create_user(self):
        """
        See if we can successfully create a new user.
        Post-condition: user is in DB.
        """
        cu = ep.CreateUser(Resource)
        new_user = new_entity_name("user")
        cu.post(new_user)
        users = db.get_users()
        self.assertIn(new_user, users)

    def test_delete_user(self):
        """
        See if we can successfully delete a user.
        Post-condition: user no longer in DB.
        """
        usrname = "delete_test_user"
        db.add_user(usrname)
        ep.DeleteUser(Resource).post(usrname)
        users = db.get_users()
        self.assertFalse((usrname in users))

    def test_list_users(self):
        """
        See if we can successfully list all users.
        Post-condition: nothing changes.
        """
        ret = ep.GetUsers(Resource).get()
        users = db.get_users()
        res = []
        for user in users:
            item = {
                "userName": users[user]['userName'],
                "profile_pic_url": users[user]['profile_pic_url']
            }
            res.append(item)
        msg = "test_list_users: Error, returned users aren't equivalent to database users"
        self.assertEqual(ret, res, msg)

    def test_create_event(self):
        """
        See if we can successfully create a new event.
        Post-condition: event is in DB.
        """
        cr = ep.CreateEvent(Resource)
        new_event = new_entity_name("event")
        ret = cr.post("test_user", new_event)
        events = db.get_events("test_user")
        self.assertIn(ret['id'], events)

    def test_delete_event(self):
        """
        See if we can successfully delete a event.
        Post-condition: event no longer in DB.
        """
        event = db.add_event("testEvent",
                             "testLoc",
                             1640146943,
                             1640146943,
                             "test descr",
                             "Paul",
                             ["Paul"])
        ep.DeleteEvent(Resource).post(event['id'])
        events = db.get_events("Paul")
        self.assertFalse((event['id'] in events))

    def test_list_events(self):
        """
        See if we can successfully list all events.
        Post-condition: noting changes.
        """
        db.add_event("testEvent",
                     "testLoc",
                     1640146943,
                     1640146943,
                     "test descr",
                     "Paul",
                     ["Paul"])
        ret = ep.ListEvents(Resource).get("Paul")
        events = db.get_events("Paul")
        msg = "test_list_events: Error, returned events aren't equivalent to database events"
        self.assertEqual(ret, events, msg)

    def test1_event(self):
        """
        Post-condition 1: return is a dictionary.
        """
        db.add_event("testEvent",
                     "testLoc",
                     1640146943,
                     1640146943,
                     "test descr",
                     "Paul",
                     ["Paul"])
        ret = ep.ListEvents(Resource).get("Paul")
        self.assertIsInstance(ret, dict)

    def test2_event(self):
        """
        Post-condition 2: keys to the dict are strings
        """
        db.add_event("testEvent",
                     "testLoc",
                     1640146943,
                     1640146943,
                     "test descr",
                     "Paul",
                     ["Paul"])
        ret = ep.ListEvents(Resource).get("Paul")
        for key in ret:
            self.assertIsInstance(key, str)

    def test3_event(self):
        """
        Post-condition 3: the values in the dict are themselves dicts
        """
        db.add_event("testEvent",
                     "testLoc",
                     1640146943,
                     1640146943,
                     "test descr",
                     "Paul",
                     ["Paul"])
        ret = ep.ListEvents(Resource).get("Paul")
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_create_break(self):
        """
        See if we can successfully create a new break.
        Post-condition: break is in DB.
        """
        cr = ep.CreateBreak(Resource)
        new_break = new_entity_name("Break")
        ret = cr.post("test_user", new_break)
        events = db.get_breaks("test_user")
        self.assertIn(ret['id'], events)

    def test_delete_break(self):
        """
        See if we can successfully delete a break.
        Post-condition: break no longer in DB.
        """
        new_break = new_entity_name("Break")
        breakItem = db.add_break(new_break, 1640146943, 1640146943, "Paul")
        ep.DeleteBreak(Resource).post(breakItem['id'])
        breaks = db.get_breaks("Paul")
        self.assertFalse((breakItem['id'] in breaks))
        
    def test_list_breaks(self):
        """
        See if we can successfully list all events.
        Post-condition: noting changes.
        """
        db.add_break("testEvent",
                     1640146943,
                     1640146943,
                     "Paul")
        ret = ep.ListBreaks(Resource).get("Paul")
        events = db.get_breaks("Paul")
        msg = "test_list_breaks: Error, returned breaks aren't equivalent to database breaks"
        self.assertEqual(ret, events, msg)

    def test1_break(self):
        """
        Post-condition 1: return is a dictionary.
        """
        db.add_break("testEvent",
                     1640146943,
                     1640146943,
                     "Paul")
        ret = ep.ListBreaks(Resource).get("Paul")
        self.assertIsInstance(ret, dict)

    def test2_break(self):
        """
        Post-condition 2: keys to the dict are strings
        """
        db.add_break("testEvent",
                     1640146943,
                     1640146943,
                     "Paul")
        ret = ep.ListBreaks(Resource).get("Paul")
        for key in ret:
            self.assertIsInstance(key, str)

    def test3_break(self):
        """
        Post-condition 3: the values in the dict are themselves dicts
        """
        db.add_break("testEvent",
                     1640146943,
                     1640146943,
                     "Paul")
        ret = ep.ListBreaks(Resource).get("Paul")
        for val in ret.values():
            self.assertIsInstance(val, dict)
