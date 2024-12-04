
import boto3
from botocore.exceptions import ClientError
import logging
logger = logging.getLogger(__name__)



class BedrockAgentService:
    def __init__(self, agent_id, alias_id="TSTALIASID", client=None) -> None:
        self.agents_runtime_client = (
            client if client else boto3.client("bedrock-agent-runtime")
        )
        self.agent_id = agent_id
        self.alias_id = alias_id

    def parse_parameters(self, parameters):
        parsed_parameters = {}
        for param in parameters:
            parsed_parameters[param["name"]] = param["value"]
        return parsed_parameters

    def return_control(self, completion):
        rc = completion.get("returnControl")
        invocationId = rc.get("invocationId")
        invocationInputs = rc.get("invocationInputs")
        functionInvocationInput = invocationInputs[0].get("functionInvocationInput")
        actionGroup = functionInvocationInput.get("actionGroup")
        actionInvocationType = functionInvocationInput.get("actionInvocationType")
        functionName = functionInvocationInput.get("function")
        parameters = functionInvocationInput.get("parameters")
        parsed_parameters = self.parse_parameters(parameters)
        return {
            "actionGroup": actionGroup,
            "functionName": functionName,
            "parameters": parsed_parameters,
            "invocationId": invocationId,
            "actionInvocationType": actionInvocationType,
        }

    def return_control_invocation_results(
        self, session_id, invocation_id, action_group, function_name, invocation_result
    ):
        try:
            response = self.agents_runtime_client.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.alias_id,
                sessionId=session_id,
                sessionState={
                    "invocationId": invocation_id,
                    "returnControlInvocationResults": [
                        {
                            "functionResult": {
                                "actionGroup": action_group,
                                "function": function_name,
                                "responseBody": {"TEXT": {"body": invocation_result}},
                            }
                        }
                    ],
                },
            )

            completion = ""

            for event in response.get("completion"):
                if event.get("returnControl"):
                    return self.return_control(event)
                chunk = event["chunk"]
                completion = completion + chunk["bytes"].decode()

        except ClientError as e:
            logger.error(f"Couldn't invoke agent. {e}")
            raise

        return completion

    # from https://docs.aws.amazon.com/code-library/latest/ug/python_3_bedrock-agent-runtime_code_examples.html
    def invoke_agent(self, session_id, prompt):
        try:
            response = self.agents_runtime_client.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.alias_id,
                sessionId=session_id,
                inputText=prompt,
            )

            completion = ""

            for event in response.get("completion"):
                if event.get("returnControl"):
                    return self.return_control(event)
                chunk = event["chunk"]
                completion = completion + chunk["bytes"].decode()

        except ClientError as e:
            logger.error(f"Couldn't invoke agent. {e}")
            raise

        return completion