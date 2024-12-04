import os
import json
from dialog_service import DialogService
from bedrock_agent import BedrockAgentService

AGENT_ID = os.environ.get("AGENT_ID")
AGENT_ALIAS_ID = os.environ.get("AGENT_ALIAS_ID")


def lambda_handler(event, context):
    print("event: ", event)

    dialog_service = DialogService(event)

    print(f"User Utterance: {dialog_service.user_utterance}")

    if dialog_service.user_utterance == "":
        return dialog_service.elicit_intent(
            [
                {
                    "contentType": "PlainText",
                    "content": "No te entendí... puedes repetir?",
                }
            ]
        )

    session_id = dialog_service.sessionId

    support_agent = BedrockAgentService(AGENT_ID, AGENT_ALIAS_ID)
    agent_response = support_agent.invoke_agent(
        session_id, dialog_service.user_utterance
    )

    print(f"Agent Response: {agent_response}")

    if type(agent_response) == str:
        return dialog_service.elicit_intent(
            [{"contentType": "PlainText", "content": agent_response}]
        )

    elif type(agent_response) == dict: 
        
        functionName = agent_response.get("functionName")

        if functionName == "escalate":  # Agent signal for escalation
            
            # get the Agent information about escalation
            invocationId = agent_response.get("invocationId")
            function_name = agent_response.get("functionName")
            action_group = agent_response.get("actionGroup")
            parameters = agent_response.get("parameters")

            print(f"escalando : {json.dumps(parameters)}")
            
            dialog_service.intent["name"] = "AgentIntent"
            dialog_service.session_attributes["previous_intent"] = "AgentIntent"

            for param in parameters: # set the escalation paramas to session state
                dialog_service.session_attributes[param] = parameters[param]

            # This is optional.
            # Just in case you need to inform the Bedrock agent about the result of the escalation (sending an email or notify someone)
            escalation_response = support_agent.return_control_invocation_results(
                session_id, invocationId, action_group, function_name, "escalate success!"
            )

            print(f"Escalation Response: {escalation_response}")

            #Now we tell lex that the intent is AgentIntent should handle the rest 
            return dialog_service.delegate()
