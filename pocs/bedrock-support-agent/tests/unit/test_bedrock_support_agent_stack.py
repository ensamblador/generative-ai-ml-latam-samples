import aws_cdk as core
import aws_cdk.assertions as assertions

from bedrock_support_agent.bedrock_support_agent_stack import BedrockSupportAgentStack

# example tests. To run these tests, uncomment this file along with the example
# resource in bedrock_support_agent/bedrock_support_agent_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BedrockSupportAgentStack(app, "bedrock-support-agent")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
