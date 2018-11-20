#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from datetime import datetime
import io

CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class VietBot(object):
    """ VietBot class wrapper
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except:
            self.config = None

        self.start_blocking()

    def _create_today_menu(self, dish):
        menu_of_the_day = "Today, you can eat {}.".format(dish)
        return menu_of_the_day

    def _create_day_menu(self, day, dish):
        menu_of_the_day = "On {}, you will be able to eat {}.".format(day, dish)
        return menu_of_the_day

    def askmenu_callback(self, hermes, intent_message):
        hermes.publish_end_session(intent_message.session_id, "")

        menu_dict = {
            "Monday": "beef meatballs or chicken with vegetables",
            "Tuesday": "roasted chicken or spicy pork",
            "Wednesday": "beef with vegetables or sweet and sour shrimps",
            "Thursday": "curry chicken or pineapple duck",
            "Friday": "pork meatballs or sweet and sour fish"
        }

        if intent_message.slots.menuday:
            str_menu_day = intent_message.slots.menuday.first().value
            dt_menu_day = datetime.strptime(str_menu_day, '%Y-%m-%d %H:%M:%S +00:00')
        else:
            dt_menu_day = datetime.now()

        dt_today = datetime.now()
        day_name = dt_menu_day.strftime("%A")

        if dt_today.date() != dt_menu_day.date():
            sentence = self._create_day_menu(day_name, menu_dict[day_name])
        else:
            sentence = self._create_today_menu(menu_dict[day_name])

        hermes.publish_start_session_notification(intent_message.site_id, sentence, "VietBot APP")

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self, hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'redTitan:WhatsOnTheMenu':
            self.askmenu_callback(hermes, intent_message)

    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    VietBot()