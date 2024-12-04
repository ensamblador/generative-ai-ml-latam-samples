#!/usr/bin/env python3
import os

import aws_cdk as cdk

from bedrock_support_agent.bedrock_support_agent_stack import BedrockSupportAgentStack


app = cdk.App()
BedrockSupportAgentStack(app, "BedrockSupportAgentStack")

app.synth()
