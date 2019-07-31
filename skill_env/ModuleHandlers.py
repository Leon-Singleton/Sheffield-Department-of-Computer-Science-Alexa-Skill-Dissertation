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

#method to handle module SQL requests
#takes paramters concerning the information requested about the module and searches
#using the one of either the modulecode or modulename slot values
def ModuleInfo(information, moduleCode, moduleName):

    #checks to see which of the two module slot values has been filled
    #then using the filled slot executes a SQL query to get the relevant
    #information requested
    with conn.cursor() as cur:
        filledSlot = ""
        if (moduleCode is None):
            filledSlot=moduleName
            sql= "SELECT " + information + " FROM Modules WHERE ModuleName=%s"
        else:
            filledSlot=moduleCode
            sql= "SELECT " + information + " FROM Modules WHERE ModuleCode=%s"
        cur.execute(sql, (filledSlot))
        speech_text = cur.fetchone()
        cur.close

    #returns the answer obtained from the SQL query
    return speech_text[0]

###################################################
# know about a module in a series of dialog turns
###################################################

#handles the instance a user asks about a module
class ModuleIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        #sets the moduleDialogTurn sesion attribute to 1 as the dialog flow has been initiated
        if (session_attr['moduleDialogTurn'] == 0):
            session_attr['moduleDialogTurn'] +=1

        session_attr['moduleDialogEnd'] = 1

        #sets a session attribute regarding the module that the user has asked about
        #if the user has asked via the module code then the corresponding module name is
        #obtained and hence used as the session attribute
        if (moduleCode is None):
            session_attr['moduleName'] = moduleName
        else:
            session_attr['moduleName'] = ModuleInfo("ModuleName", moduleCode, moduleName)

        #builds the speech response by obtaining the necessary information via the moduleinfo method
        speech_text = ModuleInfo("Summary", moduleCode, moduleName) + " Would you like to hear more?"
        session_attr['lastSpeech'] = speech_text

        reprompt= "Would you like to hear more?"

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the isntance the user replies yes when asked if they would like to hear more
#information about the module in the dialog flow
class YesMoreModuleInfoIntentHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool
         session_attr = handler_input.attributes_manager.session_attributes
         return (is_intent_name("AMAZON.YesIntent")(handler_input) and
                 session_attr['moduleDialogTurn'] != 0)

     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
         session_attr = handler_input.attributes_manager.session_attributes

         session_attr['moduleDialogEnd'] = 0
         speech_text = ""
         moduleName = session_attr['moduleName']
         moduleCode = None

         #depending on the current dialog turn value, outputs the information the user asked to hear about
         #then following this asks a question about the next piece of realted module information
         if (session_attr['moduleDialogTurn'] == 1):
             speech_text = ("Would you like to know what semester " + session_attr['moduleName'] + " is taught in?")
         elif (session_attr['moduleDialogTurn'] == 2):
             speech_text = ("It is taught in the " + ModuleInfo("Session", moduleCode, moduleName) + " session." + " Would you like to know how many credits " + session_attr['moduleName'] + " is worth?")
         elif (session_attr['moduleDialogTurn'] == 3):
            speech_text = ("It is worth " + ModuleInfo("Credits", moduleCode, moduleName) + " credits." + " Would you like to know how " + session_attr['moduleName'] + " is assessed?")
         elif (session_attr['moduleDialogTurn'] == 4):
             speech_text = (ModuleInfo("Assessment", moduleCode, moduleName) + " Would you like to know who teaches " + session_attr['moduleName'] + "?")
         elif (session_attr['moduleDialogTurn'] == 5):
             speech_text = (ModuleInfo("Lecturers", moduleCode, moduleName) + " Would you like to know the aims of " + session_attr['moduleName'] + "?")
         elif (session_attr['moduleDialogTurn'] == 6):
             speech_text = (ModuleInfo("Aims", moduleCode, moduleName) + " Would you like to know the objectives of " + session_attr['moduleName'] + "?")
         elif (session_attr['moduleDialogTurn'] == 7):
             speech_text = (ModuleInfo("Objectives", moduleCode, moduleName) + " Would you like to know about the content of " + session_attr['moduleName'] + "?")
         elif (session_attr['moduleDialogTurn'] == 8):
             speech_text = (ModuleInfo("Content", moduleCode, moduleName) + " Would you like to know how " + session_attr['moduleName'] + " is taught?")
         elif (session_attr['moduleDialogTurn'] == 9):
             speech_text = (ModuleInfo("Teaching", moduleCode, moduleName) + " Would you like to know about the feedback of " + session_attr['moduleName'] + "?")
         elif (session_attr['moduleDialogTurn'] == 10):
             speech_text = (ModuleInfo("Feedback", moduleCode, moduleName) + " That is everything to know about " + session_attr['moduleName'] + ".")
             session_attr['moduleDialogTurn'] = 0
             session_attr['lastSpeech'] = speech_text
             #finally when the dialog flow reaches 10 the dialog turn session attribute is reset
             handler_input.response_builder.speak(speech_text).set_card(
                 ui.StandardCard(
                     title=("Sheffield DCS Skill"),
                     text=speech_text)).set_should_end_session(False)
             return handler_input.response_builder.response

        #increments the dialog turn value
         session_attr['moduleDialogTurn'] = (session_attr['moduleDialogTurn'] +1)
         session_attr['lastSpeech'] = speech_text

         reprompt = "Would you like to hear more?"

         handler_input.response_builder.speak(speech_text).set_card(
             ui.StandardCard(
                 title=("Sheffield DCS Skill"),
                 text=speech_text)).set_should_end_session(False).ask(reprompt)
         return handler_input.response_builder.response

#handles the isntance the user replies no when asked if they would like to hear more
#information about the module in the dialog flow
class NoSpecificModuleInfoIntentHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool
         session_attr = handler_input.attributes_manager.session_attributes
         return (is_intent_name("AMAZON.NoIntent")(handler_input) and
                 session_attr['moduleDialogTurn'] != 0)

     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
         session_attr = handler_input.attributes_manager.session_attributes

         speech_text = ""

         #depending on the current dialog turn value, outputs a speech response asking the user if
         #they would like to hear information regarding the next module attribute
         if (session_attr['moduleDialogTurn'] == 2):
             speech_text = ("Would you like to know how many credits " + session_attr['moduleName'] + " is worth?")
         elif (session_attr == 3):
            session_attr['moduleDialogTurn'] = ("Would you like to know how " + session_attr['moduleName'] + " is assessed?")
         elif (session_attr['moduleDialogTurn'] == 4):
             speech_text = ("Would you like to know who teaches " + session_attr['moduleName'] + "?")
         elif (session_attr['moduleDialogTurn'] == 5):
             speech_text = ("Would you like to know the aims of " + session_attr['moduleName'] + "?")
         elif (session_attr['moduleDialogTurn'] == 6):
             speech_text = ("Would you like to know the objectives of " + session_attr['moduleName'] + "?")
         elif (session_attr['moduleDialogTurn'] == 7):
             speech_text = ("Would you like to know about the content of " + session_attr['moduleName'] + "?")
         elif (session_attr['moduleDialogTurn'] == 8):
             speech_text = ("Would you like to know how " + session_attr['moduleName'] + " is taught?")
         elif (session_attr['moduleDialogTurn'] == 9):
             speech_text = ("Would you like to know about the feedback of " + session_attr['moduleName'] + "?")
         elif (session_attr['moduleDialogTurn'] == 10):
             #finally when the dialog flow reaches 10 the dialog turn session attribute is reset
             speech_text = ("That is everything to know about " + session_attr['moduleName'] + ".")
             session_attr['moduleDialogTurn'] = 0
             session_attr['lastSpeech'] = speech_text
             handler_input.response_builder.speak(speech_text).set_card(
                 ui.StandardCard(
                     title=("Sheffield DCS Skill"),
                     text=speech_text)).set_should_end_session(False)
             return handler_input.response_builder.response

         #increments the dialog turn value
         session_attr['moduleDialogTurn'] += 1
         session_attr['lastSpeech'] = speech_text

         reprompt = speech_text

         handler_input.response_builder.speak(speech_text).set_card(
             ui.StandardCard(
                 title=("Sheffield DCS Skill"),
                 text=speech_text)).set_should_end_session(False).ask(reprompt)
         return handler_input.response_builder.response

#handles the instance where the user responds no when asked if they would like any more
#imformation about the module in the dialog flow
class NoMoreModuleInfoIntentHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool
         session_attr = handler_input.attributes_manager.session_attributes
         return (is_intent_name("AMAZON.NoIntent")(handler_input) and
                 session_attr['moduleDialogEnd'] == 1)

     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
         session_attr = handler_input.attributes_manager.session_attributes

         #resets the dialog flow turn session attribute
         session_attr['moduleDialogTurn'] = 0
         session_attr['moduleDialogEnd'] = 0

         speech_text = "Ok, you can ask me about another module if you like."
         session_attr['lastSpeech'] = speech_text

         reprompt = "Try asking me something else."

         handler_input.response_builder.speak(speech_text).set_card(
             ui.StandardCard(
                 title=("Sheffield DCS Skill"),
                 text=speech_text)).set_should_end_session(False).ask(reprompt)
         return handler_input.response_builder.response

###################################################
# Know all about a module intent handler below here
###################################################

#handles the instance a user asks for information all about a specific module
class ModuleAllIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleAllIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        #gets the relevant module information from the database using the modulecode and modulename slot values
        #then stores the information obtained in variables that are used to build the speech response
        summary = ModuleInfo("Summary", moduleCode, moduleName)
        session = ModuleInfo("Session", moduleCode, moduleName)
        credits = ModuleInfo("Credits", moduleCode, moduleName)

        speech_text = summary + " It is taught in the " + session + ". and it is worth " + credits + " credits."
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

###################################################
# Single Module question intent handlers below here
###################################################

#handles the instance where a user asks for a summary of a module
class ModuleSummaryIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleSummaryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        #gets the relevant module summary from the database using the modulecode and modulename slot values
        #along with the specified information parameter (summary)
        #sets the result as the output speech
        speech_text = ModuleInfo("Summary", moduleCode, moduleName)
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

#handles the instance where a user asks for the session a module is taught in
class ModuleSessionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleSessionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        speech_text = ("It is taught in the " + ModuleInfo("Session", moduleCode, moduleName) + " session.")
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user asks for the credits of a module
class ModuleCreditsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleCreditsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        speech_text = ("It is worth " + ModuleInfo("Credits", moduleCode, moduleName) + " credits.")
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

#handles the instance where a user asks for about the assessment of a module
class ModuleAssessmentIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleAssessmentIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        speech_text = ModuleInfo("Assessment", moduleCode, moduleName)
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user asks for the lecturers of a module
class ModuleLecturersIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleLecturersIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        speech_text = ModuleInfo("Lecturers", moduleCode, moduleName)
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user asks for about the aims of a module
class ModuleAimsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleAimsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        speech_text = ModuleInfo("Aims", moduleCode, moduleName)
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user asks for about the objectives of a module
class ModuleObjectivesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleObjectivesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        speech_text = ModuleInfo("Objectives", moduleCode, moduleName)
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user asks for about the content of a module
class ModuleContentIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleContentIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        speech_text = ModuleInfo("Content", moduleCode, moduleName)
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user asks for about the teaching of a module
class ModuleTeachingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleTeachingIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        speech_text = ModuleInfo("Teaching", moduleCode, moduleName)
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

#handles the instance where a user asks for about the feedback of a module
class ModuleFeedbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleFeedbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        moduleCode = handler_input.request_envelope.request.intent.slots["ModuleCode"].value
        moduleName = handler_input.request_envelope.request.intent.slots["ModuleName"].value

        speech_text = ModuleInfo("Feedback", moduleCode, moduleName)
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response
