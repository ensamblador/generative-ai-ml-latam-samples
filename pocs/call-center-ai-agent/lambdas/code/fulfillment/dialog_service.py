import json


class DialogService:
    def __init__(self, event) -> None:
        self.intent = self.get_intent(event)
        self.intent_name = self.get_intent_name()
        self.active_contexts = self.get_active_contexts(event)
        self.session_attributes = self.get_session_attributes(event)
        self.user_utterance = event.get("inputTranscript", "")
        self.sessionId = event.get('sessionId')


    def get_intent(self, intent_request):
        interpretations = intent_request['interpretations']
        if len(interpretations) > 0:
            return interpretations[0]['intent']
        else:
            return None
    
    def get_intent_name(self):
        if self.intent:
            return self.intent.get('name')
        else:
            return "FallbackIntent"

    def get_active_contexts(self, intent_request):
        """Get active contexts from the request."""
        return intent_request['sessionState'].get('activeContexts', [])
    
    def get_session_attributes(self, intent_request):
        """Get session attributes from the request."""
        return intent_request['sessionState'].get('sessionAttributes', {})

    def elicit_intent(self, messages):

        self.intent['state'] = 'Fulfilled'
        self.active_contexts = self.remove_inactive_context(self.active_contexts)
        if not self.session_attributes:
            self.session_attributes = {}
        self.session_attributes['previous_message'] = json.dumps(messages)
        self.session_attributes['previous_dialog_action_type'] = 'ElicitIntent'
        self.session_attributes['previous_slot_to_elicit'] = None
        self.session_attributes['previous_intent'] = self.intent['name']
        
        return {
            'sessionState': {
                'sessionAttributes': self.session_attributes,
                'activeContexts': self.active_contexts,
                'dialogAction': {
                    'type': 'ElicitIntent'
                },
                "state": "Fulfilled"
            },
            'requestAttributes': {},
        'messages': messages
        }

    def remove_inactive_context(self, context_list):
        if not context_list:
            return context_list
        new_context = []
        for context in context_list:
            time_to_live = context.get('timeToLive')
            if  time_to_live and time_to_live.get('turnsToLive') != 0:
                new_context.append(context)
        return new_context

    def delegate(self):
        print ('delegate!')
        self.active_contexts = self.remove_inactive_context(self.active_contexts)
        return {
            'sessionState': {
                'activeContexts': self.active_contexts,
                'sessionAttributes': self.session_attributes,
                'dialogAction': {
                    'type': 'Delegate'
                },
                'intent': self.intent,
                'state': 'ReadyForFulfillment'
            }
        }
