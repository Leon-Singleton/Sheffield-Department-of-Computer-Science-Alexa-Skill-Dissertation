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

#method to handle courses SQL requests
#takes paramters concerning the information requested about the course and searches
#using the course name of the course supplied
def CourseInfo(information, courseName):

    with conn.cursor() as cur:

        sql= "SELECT " + information + " FROM Courses WHERE CourseName=%s"
        cur.execute(sql, (courseName))
        speech_text = cur.fetchone()
        cur.close

    #returns the answer obtained from the SQL query
    return speech_text[0]

#handles the instance where a user asks about the courses offered
class CoursesOfferedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CoursesOfferedIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        speech_text = "Are you interested in postgraduate or undergraduate courses?"

        session_attr['lastSpeech'] = speech_text
        #begins a dialogflow and sets the turn of the flow to one
        session_attr['coursesDialogTurn'] = 1

        reprompt=speech_text

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance the user replies to the first stage of the courses offered dialog flow
class CoursesOfferedFlowIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("CoursesOfferedFlowIntent")(handler_input) and
                session_attr['coursesDialogTurn'] == 1)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #gets the slot value of the course type specified by the user
        courseType = handler_input.request_envelope.request.intent.slots["CourseType"].value

        #outputs the appropriate answer based on whether the user specifics undergraduate or
        #postgraduate courses
        if (courseType == "under graduate" or courseType == "undergraduate"):
            speech_text = "The Department of Computer Science offers undergraduate degrees in Computer Science, Software Engineering and Computer Science and Artificial Intelligence; all of which have an option for a Year in Industry or an Integrated Masters. Would you like more information about any of these courses?"
        else:
            speech_text = "The Department of Computer Science offers masters degrees in Advanced Computer Science, Advanced Software Engineering, Data Analytics, Software Systems and Internet Technology, Cybersecurity and Artificial Intelligence and Computer Science with Speech and Language Processing. Would you like more information about any of these courses?"

        session_attr['lastSpeech'] = speech_text
        #sets the turn of the dialogue flow to two
        session_attr['coursesDialogTurn'] = 2

        reprompt = "Would you like more information about any of the courses?"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance the user with a "yes" response to the second stage of the Course
#dialog flow
class YesCoursesOfferedFlowIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.YesIntent")(handler_input) and
                session_attr['coursesDialogTurn'] == 2)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        #if the user answers Yes, it implies they want to know further information
        #about the courses offered
        speech_text = "Which course are you interested in?"

        session_attr['lastSpeech'] = speech_text
        #sets the turn of the dialogue flow to three
        session_attr['coursesDialogTurn'] = 3

        reprompt = speech_text

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance the user with a "no" response to the second stage of the Course
#dialog flow
class NoCoursesOfferedFlowIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.NoIntent")(handler_input) and
                session_attr['coursesDialogTurn'] == 2)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        #if the user answers no, it implies they do not want to know any further information
        #and as such the coursesDialogTurn session attribute is reset
        speech_text = "Ok, you can ask me another question if you like."
        session_attr['coursesDialogTurn'] = 0

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance the user response to the third stage of the Course
#dialog flow and specifies a course they would like to hear more about
class CourseInfoFlowIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("CourseInfoFlowIntent")(handler_input) and
                session_attr['coursesDialogTurn'] == 3)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        courseName = handler_input.request_envelope.request.intent.slots["CourseName"].value

        #builds the response using the courseInfo method to obtain the information from the
        #database related to the course the user wants to hear more about
        speech_text = CourseInfo("Description", courseName) + " The UCAS code for " + courseName + " is " + CourseInfo("UcasCode", courseName) + " and the entry rquirements are " + CourseInfo("EntryReq", courseName)
        session_attr['lastSpeech'] = speech_text

        #the dialog flow is complete and so the coursesDialogTurn sesion attribute is reset
        session_attr['coursesDialogTurn'] = 0

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where the user asks about a year in industry
class IndustryYearIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("IndustryYearIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        speech_text = "You can enhance your career prospects even further by taking a year in industry as part of your degree. We have a dedicated officer who can help you find a placement. You'll be paid a salary and your University fees are reduced for that year."
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where the user asks about a specific course
class CourseInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CourseInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get value from slot
        courseName = handler_input.request_envelope.request.intent.slots["CourseName"].value

        #builds the response using the courseInfo method to obtain the information from the
        #database related to the course the user wants to hear about
        speech_text = CourseInfo("Description", courseName)
        speech_text = speech_text + " would you like to hear more about " + courseName + "?"
        session_attr['courseName'] = courseName
        session_attr['coursesHearMoreDialogTurn'] = 3
        session_attr['lastSpeech'] = speech_text
        session_attr['coursesDialogTurn'] = 0

        reprompt = "Would you like to hear more about " + courseName + "?"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where the user asks about the UCAS code a specific course
class CourseCodeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CourseCodeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get value from slot
        courseName = handler_input.request_envelope.request.intent.slots["CourseName"].value

        #builds the response using the courseInfo method to obtain the information from the
        #database related to the course the user wants to hear the UCAS code for
        speech_text = "The UCAS code for " + courseName + " is " + CourseInfo("UcasCode", courseName)
        speech_text = speech_text + " would you like to hear more about " + courseName + "?"

        session_attr['courseName'] = courseName
        session_attr['lastSpeech'] = speech_text
        session_attr['coursesHearMoreDialogTurn'] = 2
        session_attr['coursesDialogTurn'] = 0

        reprompt = "Would you like to hear more about " + courseName + "?"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where the user asks about the entry requirements of a specific course
class CourseEntryIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CourseEntryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get value from slot
        courseName = handler_input.request_envelope.request.intent.slots["CourseName"].value

        #builds the response using the courseInfo method to obtain the information from the
        #database related to the course the user wants to know the entry requirements of
        speech_text = "The entry requirements for " + courseName + " are " + CourseInfo("EntryReq", courseName)
        speech_text = speech_text + " would you like to hear more about " + courseName + "?"

        session_attr['courseName'] = courseName
        session_attr['lastSpeech'] = speech_text
        session_attr['coursesHearMoreDialogTurn'] = 1
        session_attr['coursesDialogTurn'] = 0

        reprompt = "Would you like to hear more about " + courseName + "?"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user replies yes to wanting to hear more about a specific course
class CoursesHearMoreIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.YesIntent")(handler_input) and
                session_attr['coursesHearMoreDialogTurn'] != 0)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        courseName = session_attr['courseName']


        #the responses formed depend on the value of the coursesHearMoreDialogTurn session attribute,
        #this session attribute is used to keep track of course informaion the user asked for so that when they
        #reply yes to wanting to hear more about a specific course the further information is relevant
        if (session_attr['coursesHearMoreDialogTurn'] == 1):
            #builds the speech response using the coursename session attribute and an information parameter
            #to get the relevant informatino from the database
            speech_text = CourseInfo("Description", courseName) + " The UCAS code for " + courseName + " is " + CourseInfo("UcasCode", courseName)
        elif (session_attr['coursesHearMoreDialogTurn'] == 2):
            speech_text = CourseInfo("Description", courseName) + " The the entry rquirements are " + courseName + " is " + CourseInfo("EntryReq", courseName)
        else:
            speech_text = "The UCAS code for " + courseName + " is " + CourseInfo("UcasCode", courseName) + " and the entry rquirements are " + CourseInfo("EntryReq", courseName)

        #resets the turn session attribute
        session_attr['coursesHearMoreDialogTurn'] = 0
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user replies no to wanting to hear more about a specific course
class CoursesNotHearMoreIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.NoIntent")(handler_input) and
                session_attr['coursesHearMoreDialogTurn'] != 0)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        speech_text = "Ok, you can ask me another question if you like."
        #resets the turn session attribute
        session_attr['coursesHearMoreDialogTurn'] = 0
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response
