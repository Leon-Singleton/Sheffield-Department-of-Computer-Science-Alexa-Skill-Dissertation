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

#method to handle lecturer SQL requests
#takes paramters concerning the information requested about the lecturer and searches
#using the firstname and surname of the lecturer supplied
def LecturerInfo(information, firstname, surname):

    #executes a SQL LIKE query to get information regarding a lecturer from the database
    with conn.cursor() as cur:
        sql= "SELECT " + information + " FROM Lecturers WHERE firstname LIKE '%" + firstname + "%' OR Surname LIKE '%" + surname + "%'"
        cur.execute(sql)
        speech_text = cur.fetchone()
        cur.close

    #returns the answer obtained from the SQL query
    return speech_text[0]

#method to get the other name of the lecturer if only one of either the
#firstname or surname is supplied
def getMissingName(name, slot):

    #executes a SQL LIKE query to get the missing name of the lecturer by querying using
    #the one name supplied
    with conn.cursor() as cur:
        sql= "SELECT " + name + " FROM Lecturers WHERE firstname LIKE '%" + slot + "%' OR Surname LIKE '%" + slot + "%'"
        cur.execute(sql)
        name = cur.fetchone()
        cur.close

    #returns the missing name returned from the SQL query
    return name[0]

#handles the istance where a user asks how to contact a given lecturer
class LecturerContactIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LecturerContactIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        firstname = handler_input.request_envelope.request.intent.slots["LecturerFname"].value
        surname = handler_input.request_envelope.request.intent.slots["LecturerSname"].value

        #if one of either the firstname or surname has not been supplied the method
        #getMissingName is called to obtain the missing name
        if (firstname is None):
            surname = getMissingName("Surname", surname)
        if (surname is None):
            firstname = getMissingName("Firstname", firstname)

        #obtain values for the telephone and email address of the given lecturer
        #using their firstname and surname of the lecturer calling the Lecturerinfo method
        tel = LecturerInfo("Telephone", firstname, surname)
        email = LecturerInfo("EmailAddress", firstname, surname)

        #builds the response

        #a validation check is performed to check that a telephone and EmailAddress
        #exists for the given lecturer
        if (tel is None):
            speech_text = "The email address for " + firstname + " " + surname + " is: " + email
        elif (email is None):
            speech_text = "The contact number for " + firstname + " " + surname + " is: " + tel
        elif (email is None and tel is None):
            speech_text = "There is no contact detals assocaited with " + firstname + " " + surname
        else:
            speech_text = "The email address for " + firstname + " " + surname + " is: " + email + " and their contact number is: " + tel

        #asks a follow up question and initiialises the session attributes associated with
        #dialog flow for wanting to hear more about a given lecturer
        session_attr['lecturersDialogTurn'] = 1
        speech_text = speech_text + ". Would you like to hear more about " + firstname + " " + surname + " ?"
        session_attr['lecturerFname'] = firstname
        session_attr['lecturerSname'] = surname
        session_attr['lastSpeech'] = speech_text

        reprompt = "Would you like to hear more about " + firstname + " " + surname + "?"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the isntance where a user asks about the research group of a lecturer
class LecturerGroupIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LecturerGroupIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        firstname = handler_input.request_envelope.request.intent.slots["LecturerFname"].value
        surname = handler_input.request_envelope.request.intent.slots["LecturerSname"].value

        #if one of either the firstname or surname has not been supplied the method
        #getMissingName is called to obtain the missing name
        if (firstname is None):
            surname = getMissingName("Surname", surname)
        if (surname is None):
            firstName = getMissingName("Firstname", firstname)

        #builds the response using the firstname and surname of the lecturer and by
        #obtaining the information requested using the Lecturerinfo method
        group = LecturerInfo("ResearchGroup", firstname, surname)

        #validates whether a research group exists for the given lecturer
        if (group is None):
            speech_text = "No information exists regarding the research group of " + firstname + " " + surname
        else:
            speech_text = firstname + " " + surname + " is a " + group

        #asks a follow up question and initiialises the session attributes associated with
        #dialog flow for wanting to hear more about a given lecturer
        session_attr['lecturersDialogTurn'] = 1
        speech_text = speech_text + ". Would you like to hear more about " + firstname + " " + surname + "?"
        session_attr['lecturerFname'] = firstname
        session_attr['lecturerSname'] = surname
        session_attr['lastSpeech'] = speech_text

        reprompt = "Would you like to hear more about " + firstname + " " + surname + "?"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user asks for information about a specific lecturer
class LecturerInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LecturerInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        firstname = handler_input.request_envelope.request.intent.slots["LecturerFname"].value
        surname = handler_input.request_envelope.request.intent.slots["LecturerSname"].value

        #if one of either the firstname or surname has not been supplied the method
        #getMissingName is called to obtain the missing name
        if (firstname is None):
            surname = getMissingName("Surname", surname)
        if (surname is None):
            firstname = getMissingName("Firstname", firstname)

        #builds the response using the firstname and surname of the lecturer and by
        #obtaining the information requested using the Lecturerinfo method
        bibliography = LecturerInfo("Bibliography", firstname, surname)

        #validates whether a bibliography exists for the given lecturer
        if (bibliography is None):
            speech_text = "A bibliography does not exist for " + firstname + " " + surname
        else:
            speech_text = bibliography

        #asks a follow up question and initiialises the session attributes associated with
        #dialog flow for wanting to hear more about a given lecturer
        speech_text = speech_text + " would you like to know how to contact " + firstname + " " + surname + "?"
        session_attr['lecturerFname'] = firstname
        session_attr['lecturerSname'] = surname
        session_attr['lecturersDialogTurn'] = 2
        session_attr['lastSpeech'] = speech_text

        reprompt = "Would you like to know how to contact " + firstname + " " + surname + "?"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user replies yes to wanting to hear more about a specific lecturer
class LecturerHearMoreIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.YesIntent")(handler_input) and
                session_attr['lecturersDialogTurn'] != 0)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        #gets the firstanme and surname stored in the corresponding session attributes
        firstname = session_attr['lecturerFname']
        surname = session_attr['lecturerSname']

        if (session_attr['lecturersDialogTurn'] == 2):
            #obtain values for the telephone and email address of the given lecturer
            #using their firstname and surname of the lecturer calling the Lecturerinfo method
            tel = LecturerInfo("Telephone", firstname, surname)
            email = LecturerInfo("EmailAddress", firstname, surname)

            #a validation check is performed to check that a telephone and EmailAddress
            #exists for the given lecturer
            if (tel is None):
                speech_text = "The email address for " + firstname + " " + surname + " is: " + email
            elif (email is None):
                speech_text = "The contact number for " + firstname + " " + surname + " is: " + tel
            elif (email is None and tel is None):
                speech_text = "There is no contact detals assocaited with " + firstname + " " + surname
            else:
                speech_text = "The email address for " + firstname + " " + surname + " is: " + email + " and their contact number is: " + tel
        else:
            #builds the response using the firstname and surname of the lecturer and by
            #obtaining the information requested using the Lecturerinfo method
            bibliography = LecturerInfo("Bibliography", firstname, surname)
            #a validation check is performed to check that a bibliography exists for the
            #given lecturer
            if (bibliography is None):
                speech_text = "A bibliography does not exist for " + firstname + " " + surname
            else:
                speech_text = bibliography

        #resets the turn session attribute
        session_attr['lecturersDialogTurn'] = 0
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user replies no to wanting to hear more about a specific lecturer
class LecturerNotHearMoreIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.NoIntent")(handler_input) and
                session_attr['lecturersDialogTurn'] != 0)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        speech_text = "Ok, you can ask me another question if you like."

        #resets the turn session attribute
        session_attr['lecturersDialogTurn'] = 0
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user replies no to wanting to hear more about a specific lecturer
class LecturerTeachesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LecturerTeachesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        firstname = handler_input.request_envelope.request.intent.slots["LecturerFname"].value
        surname = handler_input.request_envelope.request.intent.slots["LecturerSname"].value

        #if one of either the firstname or surname has not been supplied the method
        #getMissingName is called to obtain the missing name
        if (firstname is None):
            surname = getMissingName("Surname", surname)
        if (surname is None):
            firstname = getMissingName("Firstname", firstname)

        fullname = firstname + " " + surname

        #return all the modules from the database associated with the given lecturer
        with conn.cursor() as cur:
            sql= "SELECT distinct(ModuleName) FROM Modules where Lecturers LIKE '%" + fullname + "%'"
            cur.execute(sql)
            result = cur.fetchall()
            cur.close

        speech_text = "The modules taught by " + fullname + " are: "

        #recurses over the results object to build the speech output
        for x in result:
            speech_text = speech_text + x[0] + ", "

        #asks a follow up question and initiialises the session attributes associated with
        #dialog flow for wanting to hear more one of the modules that a lecturer teaches
        speech_text = speech_text + " would you like to hear more about one of these modules?"
        session_attr['lecturersModulesDialogTurn'] = 1
        session_attr['lastSpeech'] = speech_text

        reprompt = "Would you like to hear more about one of the lecturers modules?"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user replies yes to wanting to hear more about a specific lecturer's modules
class LecturerModuleHearMoreIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.YesIntent")(handler_input) and
                session_attr['lecturersModulesDialogTurn'] == 1)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        speech_text = "Which module would you like to hear more about?"

        #increments the lecturersModulesDialogTurn attribute to initiate the next
        #stage of the dialog flow
        session_attr['lecturersModulesDialogTurn'] = 2
        session_attr['lastSpeech'] = speech_text

        reprompt = speech_text

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user replies no to wanting to hear more about a specific lecturer's modules
class LecturerModuleNotHearMoreIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.NoIntent")(handler_input) and
                session_attr['lecturersModulesDialogTurn'] == 1)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        speech_text = "Ok, you can ask me another question if you like."
        #resets the turn session attribute
        session_attr['lecturersModulesDialogTurn'] = 0
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

class LecturerModuleIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("LecturerModuleIntent")(handler_input) and
                session_attr['lecturersModulesDialogTurn'] == 2)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        with conn.cursor() as cur:

            sql= "SELECT Summary FROM Modules WHERE ModuleName=%s"
            cur.execute(sql, moduleName)
            speech_text = cur.fetchone()
            cur.close

        speech_text = speech_text[0] + " Would you like to hear more?"
        #sets the moduleDialogTurn sesion attribute to 1 as the dialog flow has been initiated
        if (session_attr['moduleDialogTurn'] == 0):
            session_attr['moduleDialogTurn'] +=1

        #sets the moduleDialogEnd session attribute to true in order to initialise the
        #module dialog flow
        session_attr['moduleDialogEnd'] = True
        session_attr['moduleName'] = moduleName
        #resets the turn session attribute
        session_attr['lecturersModulesDialogTurn'] = 0

        session_attr['lastSpeech'] = speech_text

        reprompt = "Would you like to hear more about " + moduleName + "?"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response
