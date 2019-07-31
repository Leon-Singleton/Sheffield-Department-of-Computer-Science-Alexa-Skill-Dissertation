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

#handles the instance where a user asks a question that is cotained within the list of database FAQ's
class FAQIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FAQIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        #get values from slots
        question = handler_input.request_envelope.request.intent.slots["FAQ"].value

        #eliminate occurences of ' as they cause the sql string to break and crash
        question=question.replace("'", "")

        #in order to get the answer to a FAQ, the full text search mode of MYSQL has been used
        #this takes the user's question and attempts to match it against a list of questions stored
        #in the database. Then by taking the question from the database that is most similar to the
        #question (by taking the highest ranked relevance score) asked the corresponding answer is
        #retrieved and output as the speech.
        with conn.cursor() as cur:
            sql= "SELECT Answer FROM Faqs WHERE match (Question) against ('" + question + "' in natural language mode)"
            cur.execute(sql)
            speech_text = cur.fetchone()
            cur.close

        #if no answer matches question then appropraite response is output
        if (speech_text[0] is None):
            speech_text = "No answer could be found for your question, try asking something else."
        #otherwise the answer found is supplied as the response
        else:
            speech_text = speech_text[0]
        session_attr['lastSpeech'] = speech_text

        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response

from searchengine import *

#handles the instance where a user asks a question that is not cotained within the list of database FAQ's
class FAQSearchIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FAQSearchIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        request = handler_input.request_envelope.request.intent.slots["Search"].value

        #eliminate occurences of ' as they can cause the sql string to break and crash
        request=request.replace("'", "")

        #use the search engine to search the askus webpages for freqeuntly asked questions
        #matching the user's question
        results = conduct_search(request)

        if (results[0] is None):
            speech_text = "No answer could be found for your question, try asking something else."
        else:

            #set the speech output as the answer that most closely matches the user's question
            #replace any & occurences with and to avoid invalid ssml output speech
            speech_text = results[0][1].replace("&", "and")

        session_attr['lastSpeech'] = speech_text
        reprompt = "Try asking me something else."

        handler_input.response_builder.speak(speech_text).set_card(
            ui.StandardCard(
                title=("Sheffield DCS Skill"),
                text=speech_text)).set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response
