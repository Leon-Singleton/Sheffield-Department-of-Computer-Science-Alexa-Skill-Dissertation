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

#method to handle timetable SQL requests
def TimetableInfo(moduleCode, moduleName):

    with conn.cursor() as cur:

        #Checks to see if the unit code has been supplied, if not the unit code relating
        #to the supplied unitTitle is obtained.
        #This is becuase a UnitTitle can have several unitcodes meaining that there is
        #essentially duplicate timetable informatoon stored in the database.
        if (moduleCode is None):
            sql= "SELECT UnitCode FROM COMTimetables WHERE UnitTitle =%s"
            cur.execute(sql, moduleName)
            moduleCode = cur.fetchone()
            moduleCode = moduleCode[0]

        #selects all the timetable information relating to the moduleCode
        sql= "SELECT * FROM COMTimetables WHERE UnitCode =%s"
        cur.execute(sql, moduleCode)
        result = cur.fetchall()
        cur.close

    #returns the timetable information as an object
    return result

#handles the instance a user asks for timetable information concerning a module
class TimetableIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TimetableIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["TimetableUnitCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["TimetableUnitTitle"].value

        #calls the TimetableInfo method to query the database for the timetable information
        #relating to the user's request
        timetableResults=TimetableInfo(moduleCode, moduleName)

        #builds the speech output by looping over the timetableResults object and
        #selecting the columns of information from the database response that are
        #relevant to form the response.
        speech_text =""
        for x in timetableResults:
            moduleName=x[1]
            speech_text = speech_text + x[4] + " on " + x[5] + " at " + x[6] + " until " + x[7] + " in weeks " + x[8] + " of the " + x[9] + ". "

        session_attr['lastSpeech'] = speech_text
        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response
