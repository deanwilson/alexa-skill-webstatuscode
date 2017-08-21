
def alexa_handler(event, context):
    request = event['request']
    session = event['session']

    print("event.session.application.applicationId=" +
          session['application']['applicationId'])

#    if (event['session']['application']['applicationId'] !=
#             "amzn1.echo-sdk-ams.app.[unique-value-here]"):
#         raise ValueError("Invalid Application ID")

    if session['new']:
        on_session_started({'requestId': request['requestId']},
                           session)

    if request['type'] == "LaunchRequest":
        return on_launch(request, session)
    elif request['type'] == "IntentRequest":
        return on_intent(request, session)
    elif request['type'] == "SessionEndedRequest":
        return on_session_ended(request, session)


def on_session_started(session_started_request, session):

    print('on_session_started requestId=' +
          session_started_request['requestId'] +
          ', sessionId=' + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when user launches skill without specifying what they want """

    print('on_launch requestId=' + launch_request['requestId'] +
          ', sessionId=' + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_session_ended(session_ended_request, session):
    """  not called when the skill returns should_end_session=true """

    print('on_session_ended requestId=' + session_ended_request['requestId'] +
          ', sessionId=' + session['sessionId'])


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == 'WebStatusCode':
        return get_http_status(intent, session)
    elif intent_name == 'AMAZON.HelpIntent':
        return get_welcome_response()
    elif intent_name in ('AMAZON.CancelIntent', 'AMAZON.StopIntent'):
        return handle_session_end_request()
    else:
        raise ValueError('Invalid intent')


def handle_session_end_request():
    card_title = 'Thank you'
    speech_output = 'Thank you for using the Web Status Code skill.'
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))


def get_welcome_response():
    session_attributes = {}
    card_title = 'Welcome'

    speech_output = """
                    Welcome to the Alexa WebStatuscode skill.
                    You can ask me to lookup any numeric HTTP Status code
                    and I will tell you the codes name.
                    """

    reprompt_text = 'Please ask me a HTTP status code, for example 403.'

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_http_status(intent, session):
    card_title = 'Status code Results'
    session_attributes = {}
    should_end_session = True

    if 'StatusCode' in intent['slots'] and 'value' in intent['slots']['StatusCode']:
        status_code = intent['slots']['StatusCode']['value']

        explanation = code_mapping(status_code)

        session_attributes = {"statusCode": explanation}

        speech_output = status_code + ' means ' + explanation
        reprompt_text = 'You can ask me for another HTTP Status code'

    else:
        speech_output = 'I do not know that status code. Please ask me another.'
        reprompt_text = 'You can ask me for other status codes'

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def code_mapping(status_code):

    return {
        '100': 'Continue',
        '101': 'Switching Protocols',
        '102': 'Processing (WebDAV)',
        '200': 'OK',
        '201': 'Created',
        '202': 'Accepted',
        '203': 'Non-Authoritative Information',
        '204': 'No Content',
        '205': 'Reset Content',
        '206': 'Partial Content',
        '207': 'Multi-Status (WebDAV)',
        '208': 'Already Reported (WebDAV)',
        '226': 'IM Used',
        '300': 'Multiple Choices',
        '301': 'Moved Permanently',
        '302': 'Found',
        '303': 'See Other',
        '304': 'Not Modified',
        '305': 'Use Proxy',
        '306': '(Unused)',
        '307': 'Temporary Redirect',
        '308': 'Permanent Redirect (experimental)',
        '400': 'Bad Request',
        '401': 'Unauthorized',
        '402': 'Payment Required',
        '403': 'Forbidden',
        '404': 'Not Found',
        '405': 'Method Not Allowed',
        '406': 'Not Acceptable',
        '407': 'Proxy Authentication Required',
        '408': 'Request Timeout',
        '409': 'Conflict',
        '410': 'Gone',
        '411': 'Length Required',
        '412': 'Precondition Failed',
        '413': 'Request Entity Too Large',
        '414': 'Request-URI Too Long',
        '415': 'Unsupported Media Type',
        '416': 'Requested Range Not Satisfiable',
        '417': 'Expectation Failed',
        '418': "I'm a teapot (RFC 2324)",
        '420': 'Enhance Your Calm (Twitter)',
        '422': 'Unprocessable Entity (WebDAV)',
        '423': 'Locked (WebDAV)',
        '424': 'Failed Dependency (WebDAV)',
        '425': 'Reserved for WebDAV',
        '426': 'Upgrade Required',
        '428': 'Precondition Required',
        '429': 'Too Many Requests',
        '431': 'Request Header Fields Too Large',
        '444': 'No Response (Nginx)',
        '449': 'Retry With (Microsoft)',
        '450': 'Blocked by Windows Parental Controls (Microsoft)',
        '451': 'Unavailable For Legal Reasons',
        '499': 'Client Closed Request (Nginx)',
        '500': 'Internal Server Error',
        '501': 'Not Implemented',
        '502': 'Bad Gateway',
        '503': 'Service Unavailable',
        '504': 'Gateway Timeout',
        '505': 'HTTP Version Not Supported',
        '506': 'Variant Also Negotiates (Experimental)',
        '507': 'Insufficient Storage (WebDAV)',
        '508': 'Loop Detected (WebDAV)',
        '509': 'Bandwidth Limit Exceeded (Apache)',
        '510': 'Not Extended',
        '511': 'Network Authentication Required',
        '598': 'Network read timeout error',
        '599': 'Network connect timeout error',
    }.get(status_code, 'unknown')


# ---- Helpers that build all of the responses ----


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
