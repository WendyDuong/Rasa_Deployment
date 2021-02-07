# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import csv
# from database_connectivity import dataupdate
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
# from rasa_sdk.events import EventType
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, FormValidationAction
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from csv import writer
import os
os.environ['MPLCONFIGDIR'] = "/tmp"
import matplotlib


# helper functions

class FormInfo(Action):

    def name(self) -> Text:
        return "validate_form_info"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> List[
        Dict[Text, Any]]:
        required_slot = ["1_activity", "2_outside", "3_workingtime", "4_environment", "5_company", "6_skills",
                         "7_personally",
                         "8_problems_dealing", "9_public",
                         "10_min_salary", "11_wish_salary"]

        for slot_name in required_slot:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill the slot next
                return [SlotSet("required_slot", slot_name)]

        # All slots are filled
        return [SlotSet("required_slot", None)]


class ActionSubmit(Action):

    def name(self) -> Text:
        return "action_submit"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        job_workplaces = tracker.get_slot("1_activity") + tracker.get_slot("2_outside") + tracker.get_slot(
            "3_workingtime") + ("4_environment") + ("5_company")
        job_softskills = tracker.get_slot("6_skills") + tracker.get_slot("7_personally") + tracker.get_slot(
            "8_problems_dealing") + tracker.get_slot("9_public")

        # List of strings
        # Append a list as new line to an old csv file

        dispatcher.utter_message(template="utter_slots_values", activity=tracker.get_slot("1_activity"),
                                 outside=tracker.get_slot("2_outside"), workingtime=tracker.get_slot("3_workingtime"),
                                 environment=tracker.get_slot("4_environment"), company=tracker.get_slot("5_company"),
                                 skills=tracker.get_slot("6_skills"),
                                 personally=tracker.get_slot("7_personally"),
                                 problems_dealing=tracker.get_slot("8_problems_dealing"),
                                 public=tracker.get_slot("9_public"),
                                 min_salary=tracker.get_slot("10_min_salary"),
                                 wish_salary=tracker.get_slot("11_wish_salary"))
        return []
