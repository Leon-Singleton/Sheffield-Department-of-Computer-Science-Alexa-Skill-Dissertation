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
from random import *

#import the database connection information
from sqlConnection import *

#connect to the database server
conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)

#create an instance of the Alexa SkillBuilder
sb = SkillBuilder()

#handles the instance that the user invokes the skill
class LaunchRequestHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool
         return is_request_type("LaunchRequest")(handler_input)

     def handle(self, handler_input):
         # type: (HandlerInput) -> Response

         #set the initial session attributes in the attributes manager when the skill begins
         session_attr = handler_input.attributes_manager.session_attributes
         session_attr['moduleDialogEnd'] = 0
         session_attr['moduleDialogTurn'] = 0
         session_attr['coursesDialogTurn'] = 0
         session_attr['coursesHearMoreDialogTurn'] = 0
         session_attr['lecturersDialogTurn'] = 0
         session_attr['lecturersModulesDialogTurn'] = 0
         session_attr['HelpDialogRandomised'] = False

         #sets the speech output
         speech_text = "Welcome to the Sheffield Department of Computer Science Alexa Skill!"

         #this session attribute is used to remember the last piece of spoken speech
         session_attr['lastSpeech'] = speech_text

         reprompt= "Say help if you need assistance getting started."

         #This handler handles the reponse of the given intent, by setting the output speech
         #and the visual component of the skill using the card property
         handler_input.response_builder.speak(speech_text).set_card(
             ui.StandardCard(
                 title=("Sheffield DCS Skill"),
                 text=speech_text)).set_should_end_session(False).ask(reprompt)
         return handler_input.response_builder.response

#handles the instance a user invokes the help intent
class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        #Chekck if it is the first help message, if not gets a random help message from the database
        if (session_attr['HelpDialogRandomised'] == False):
            speech_text = "You can ask me about modules, courses, lecturers, timetabling information as well as general questions regarding applications. If your question cannot be answered try saying search followed by your question to query the university related webpages for an answer."
            session_attr['HelpDialogRandomised'] = True
        else:
            with conn.cursor() as cur:
                #gets the maximum id value of the last help record in the Help database table
                sql= "SELECT HelpID FROM Help ORDER BY HelpID DESC LIMIT 1;"
                cur.execute(sql)
                maxID = cur.fetchone()
                maxID = maxID[0]

                #generates a ranom number between 1 and the highest ID value of the last help message in the database
                x = randint(1, maxID)

                #used the random generated id to get a random help message
                sql= "SELECT Message FROM Help WHERE HelpID=%s"
                cur.execute(sql, (x))
                speech_text = cur.fetchone()
                #sets the speech output as the random help message
                speech_text = speech_text[0]
                cur.close

        session_attr['lastSpeech'] = speech_text
        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance a user invokes the repeat intent
class RepeatIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        #uses the last speech session attribute to output the last spoken speech
        speech_text = session_attr['lastSpeech']
        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user wants to stop using the skill,
#this is invoked by either the AMAZON.CancelIntent or AMAZON.StopIntent
class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Thanks for using the Sheffield Department of Computer Science Alexa Skill."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response

#handles the instance where a user wants to exit a conversation flow an start over
class StartOverIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.StartOverIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        speech_text = "Session restarted"
        session_attr['lastSpeech'] = speech_text

        #reset the dialogue turn session attributes
        session_attr['moduleDialogEnd'] = 0
        session_attr['moduleDialogTurn'] = 0
        session_attr['coursesDialogTurn'] = 0
        session_attr['coursesHearMoreDialogTurn'] = 0
        session_attr['lecturersDialogTurn'] = 0
        session_attr['lecturersModulesDialogTurn'] = 0

        reprompt = "Try asking me something else"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles cleanup code logic when a user closes a skill
class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response

#handles an instance where the skill cannot fulfill the user's request
class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech_text = "Sorry, I didn't quite get that. Can you please say it again?"

        reprompt = "Try asking me something else"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#imports the handlers that have been structured in files relating to their purpose
from ModuleHandlers import *
from CoursesHandlers import *
from DepartmentHandlers import *
from FavouritesHandlers import *
from LecturerHandlers import *
from TimetableHandlers import *
from FAQHandlers import *

#below here are where the intent handlers are added into the skillbuilder model

#common skill handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(StartOverIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

#module handlers
sb.add_request_handler(ModuleIntentHandler())
sb.add_request_handler(YesMoreModuleInfoIntentHandler())
sb.add_request_handler(NoMoreModuleInfoIntentHandler())
sb.add_request_handler(NoSpecificModuleInfoIntentHandler())
sb.add_request_handler(ModuleAllIntentHandler())
sb.add_request_handler(ModuleSummaryIntentHandler())
sb.add_request_handler(ModuleSessionIntentHandler())
sb.add_request_handler(ModuleCreditsIntentHandler())
sb.add_request_handler(ModuleAssessmentIntentHandler())
sb.add_request_handler(ModuleLecturersIntentHandler())
sb.add_request_handler(ModuleAimsIntentHandler())
sb.add_request_handler(ModuleObjectivesIntentHandler())
sb.add_request_handler(ModuleContentIntentHandler())
sb.add_request_handler(ModuleTeachingIntentHandler())
sb.add_request_handler(ModuleFeedbackIntentHandler())

#course handlers
sb.add_request_handler(CoursesOfferedIntentHandler())
sb.add_request_handler(CoursesOfferedFlowIntentHandler())
sb.add_request_handler(YesCoursesOfferedFlowIntentHandler())
sb.add_request_handler(NoCoursesOfferedFlowIntentHandler())
sb.add_request_handler(CourseInfoFlowIntentHandler())
sb.add_request_handler(IndustryYearIntentHandler())
sb.add_request_handler(CourseInfoIntentHandler())
sb.add_request_handler(CourseCodeIntentHandler())
sb.add_request_handler(CourseEntryIntentHandler())
sb.add_request_handler(CoursesHearMoreIntentHandler())
sb.add_request_handler(CoursesNotHearMoreIntentHandler())

#department handlers
sb.add_request_handler(DCSInfoIntentHandler())
sb.add_request_handler(DCSContactIntentHandler())
sb.add_request_handler(DCSLocationIntentHandler())

#lecturer handlers
sb.add_request_handler(LecturerContactIntentHandler())
sb.add_request_handler(LecturerInfoIntentHandler())
sb.add_request_handler(LecturerGroupIntentHandler())
sb.add_request_handler(LecturerHearMoreIntentHandler())
sb.add_request_handler(LecturerNotHearMoreIntentHandler())
sb.add_request_handler(LecturerTeachesIntentHandler())
sb.add_request_handler(LecturerModuleHearMoreIntentHandler())
sb.add_request_handler(LecturerModuleNotHearMoreIntentHandler())
sb.add_request_handler(LecturerModuleIntentHandler())

#faq handlers
sb.add_request_handler(FAQIntentHandler())
sb.add_request_handler(FAQSearchIntentHandler())

#Timetable handlers
sb.add_request_handler(TimetableIntentHandler())

#favourtie modules handlers
sb.add_request_handler(FavouriteModuleListIntentHandler())
sb.add_request_handler(FavouriteModuleAddIntentHandler())
sb.add_request_handler(FavouriteModuleDeleteIntentHandler())
sb.add_request_handler(FavouriteModuleClearIntentHandler())

#exception handlers
sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
