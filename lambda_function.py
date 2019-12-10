# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import random
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SKILL_NAME = "Massa Corporal"

def table_imc(imc):
    if imc < 16:
        return "Segundo a Organização Mundial da Saúde, seu estado nutricional é de baixo peso severo."
    elif imc >= 16 and imc < 17:
        return "Segundo a Organização Mundial da Saúde, seu estado nutricional é de baixo peso moderado."
    elif imc >= 17 and imc < 18.5:
        return "Segundo a Organização Mundial da Saúde, seu estado nutricional é de baixo peso leve."
    elif imc >= 18.5 and imc < 25:
        return "Segundo a Organização Mundial da Saúde, seu estado nutricional é considerado saudável."
    elif imc >= 25 and imc < 30:
        return "Segundo a Organização Mundial da Saúde, seu estado nutricional é de sobrepeso."
    elif imc >= 30 and imc < 35:
        return "Segundo a Organização Mundial da Saúde, seu estado nutricional é de obesidade (grau 1)."
    elif imc >= 35 and imc < 40:
        return "Segundo a Organização Mundial da Saúde, seu estado nutricional é de obesidade severa (grau 2)."
    else:
        return "Segundo a Organização Mundial da Saúde, seu estado nutricional é de obesidade mórbida (grau 3)."

instructions_ = ["O cálculo do seu índice de massa corporal poderá ser ativado quando você perguntar: estou gôrdo?",
                 "Você pode ativar o cálculo do IMC falando: calcular meu IMC.",
                 "Você pode responder simplesmente sim à essa pergunta.",
                ]  

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Você está em " + SKILL_NAME + ". Vamos calcular o seu índice de massa corporal (IMC)?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(instructions_[random.randint(0,len(instructions_)-1)])
                .response
        )

class greetingIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("greetingIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Olá! Vamos calcular o seu índice de massa corporal?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Desculpe, não entendi. Você pode ativar o cálculo perguntando, por exemplo: qual meu IMC?")
                .response
        )        

class imcIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("imcIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Ok! Vamos calcular o seu IMC. Qual a sua altura em centímetros?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Desculpe. Qual a sua altura em centímetros?")
                .response
        )

class heightIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("heightIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        heigth = int(slots['heigth'].value)
        
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["height_imc"] = heigth
        
        speak_output = "Certo. Você tem " + str(heigth) + " centímetros de altura. E qual seu peso em quilos?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Desculpe. Qual seu peso em quilos?")
                .response
        )

class weightIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("weightIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        weight = int(slots['weight'].value)
        
        session_attr = handler_input.attributes_manager.session_attributes
        heigth = session_attr["height_imc"]/100
        
        imc = weight / pow(heigth, 2)
        imc = round(imc,2)
        
        speak_output = "Certo. Você pesa " + str(weight) + " quilos. Então, o seu IMC é " + str(imc) + ". " + table_imc(imc)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Desculpe. Qual seu peso em quilos?")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "O cálculo do seu índice de massa corporal poderá ser ativado quando você perguntar: estou gôrdo?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Até a próxima!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        #speak_output = "You just triggered " + intent_name + "."
        speak_output = "Desculpe. Tive um problema. Por favor, recomece."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # ".ask("add a reprompt if you want to keep the session open for the user to respond")"
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe. Tive problemas. Podemos recomeçar?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(greetingIntentHandler())
sb.add_request_handler(imcIntentHandler())
sb.add_request_handler(heightIntentHandler())
sb.add_request_handler(weightIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
