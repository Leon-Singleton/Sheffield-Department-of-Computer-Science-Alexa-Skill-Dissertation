#import pymysql, the library used for SQL queries within python
import pymysql

#imports for the required skill development components
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import ui

#import the database connection information
from sqlConnection import *

#handles the instance a user asks for the contents of their favourites list
class FavouriteModuleListIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FavouriteModuleListIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get's the user's unique userID from their Alexa enabled device
        userID = handler_input.request_envelope.context.system.user.user_id

        #using the user's unqiue userID their previosly added favourite modules are obtained
        with conn.cursor() as cur:
            sql= "SELECT ModuleName FROM Modules, FavouriteModules where Modules.ModuleCode=FavouriteModules.ModuleCode AND FavouriteModules.UserID = %s"
            cur.execute(sql, userID)
            result = cur.fetchall()
            cur.close

        #if the result of the SQL search is an empty list then an appropriate message is output
        if result == ():
            speech_text = "Your current list of favourite modules is empty."
        #if the result is not empty then the list is recursed over each element to form the output speech
        else:
            speech_text = "Your current list of favourite modules includes: "

            for x in result:
                print(x[0])
                speech_text += x[0] + ", "

        session_attr['lastSpeech'] = speech_text
        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user wants to add a module to their favourites
class FavouriteModuleAddIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FavouriteModuleAddIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        #get's the user's unique userID from their Alexa enabled device
        userID = handler_input.request_envelope.context.system.user.user_id

        #if the user provides a module name rather than a module code then the corresponding
        #module code is obtained and set as the module code value to add to the favourites
        #list table
        with conn.cursor() as cur:
            filledSlot = ""
            if (moduleCode is None):
                filledSlot=moduleName
                sql= "SELECT ModuleCode FROM Modules WHERE ModuleName=%s"
                cur.execute(sql, (filledSlot))
                result = cur.fetchone()

                val=result[0]
            else:
                filledSlot=moduleCode
                val=moduleCode

            #verfiy module is not already in favourites list
            sql= "SELECT ModuleCode FROM FavouriteModules WHERE ModuleCode=%s AND FavouriteModules.UserID = %s"
            cur.execute(sql, (val, userID))
            result= cur.fetchone()

            #if not in favourites list then add using the moduleCode and userID values
            if result is None:

                sql= "INSERT INTO FavouriteModules (ModuleCode , UserID) VALUES (%s , %s)"
                cur.execute(sql, (val, userID))
                conn.commit()
                cur.close
                speech_text = filledSlot + " was successfully added to your list of favourite modules."
            else:
                speech_text = filledSlot + " is already in your list of favourite modules."

        session_attr['lastSpeech'] = speech_text
        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

class FavouriteModuleDeleteIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FavouriteModuleDeleteIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        #get's the user's unique userID from their Alexa enabled device
        userID = handler_input.request_envelope.context.system.user.user_id

        #if the user provides a module name rather than a module code then the corresponding
        #module code is obtained and set as the module code value to add to the favourites
        #list table
        with conn.cursor() as cur:
            filledSlot = ""
            if (moduleCode is None):
                filledSlot=moduleName
                sql= "SELECT ModuleCode FROM Modules WHERE ModuleName=%s"
                cur.execute(sql, (filledSlot))
                result = cur.fetchone()

                val=result[0]
            else:
                filledSlot=moduleCode
                val=moduleCode

            #verfiy module is in favourites list
            sql= "SELECT ModuleCode FROM FavouriteModules WHERE ModuleCode=%s AND FavouriteModules.UserID = %s"
            cur.execute(sql, (val, userID))
            result= cur.fetchone()

            #if in favourites list then delete using the users unique userID
            if result is None:
                speech_text = filledSlot + " is not currently in your list of favourite modules."
            else:
                sql= "DELETE FROM FavouriteModules WHERE ModuleCode=%s AND FavouriteModules.UserID = %s"
                cur.execute(sql, (val, userID))
                conn.commit()
                cur.close

                speech_text = filledSlot + " was successfully removed from your list of favourite modules."

        session_attr['lastSpeech'] = speech_text
        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user wants to clear the contents of their favourites
class FavouriteModuleClearIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FavouriteModuleClearIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get's the user's unique userID from their Alexa enabled device
        userID = handler_input.request_envelope.context.system.user.user_id

        #deletes all records from the favouritemodules table that match the users
        #unique userID
        with conn.cursor() as cur:
            sql= "DELETE FROM FavouriteModules WHERE FavouriteModules.UserID = %s"
            cur.execute(sql, userID)
            conn.commit()
            cur.close

        speech_text = "Your module favourites list was successfully cleared."

        session_attr['lastSpeech'] = speech_text
        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response
