import json
from aws_cdk import (Stack, aws_iam as iam)
from constructs import Construct
from lambdas import Lambdas
from databases import Tables
from bedrock_agent import Agent
from bedrock_agent.load_data import create_ag_property

# use an inference profile
DEFAULT_MODEL_ID    = "us.anthropic.claude-3-5-haiku-20241022-v1:0"

file_path_ag_data   = "./bedrock_agent/ag_data.json"

class BedrockSupportAgentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Tb = Tables(self, "Tb")
        Fn = Lambdas(self, "Fn")

        Tb.orders.grant_read_data(Fn.orders)
        Tb.tickets.grant_read_write_data(Fn.tickets)

        Fn.orders.add_environment("ORDER_TABLE_NAME", Tb.orders.table_name)
        Fn.tickets.add_environment("TICKET_TABLE_NAME", Tb.tickets.table_name)

        # To use in action groups
        Fn.orders.add_permission(
            f"invoke from Bedrock Service",
            principal=iam.ServicePrincipal("bedrock.amazonaws.com"), action="lambda:invokeFunction")
         # To use in action groups
        Fn.tickets.add_permission(
            f"invoke from Bedrock Service",
            principal=iam.ServicePrincipal("bedrock.amazonaws.com"), action="lambda:invokeFunction")





        # ======================================================================
        # Amazon Bedrock Agent Creation
        # ======================================================================
        
        # Update action groups data with functions arn 
        with open(file_path_ag_data, "r") as file:
            ag_data = json.load(file)
        
        ag_data[0]["lambda_"]= Fn.tickets.function_arn
        ag_data[1]["lambda_"]= Fn.orders.function_arn

        action_group_data = create_ag_property(ag_data)

        agent_data = {
            "agent_name": "Customer-Support",
            "description": "Agentic Customer Support.",
            "foundation_model": DEFAULT_MODEL_ID,
            "agent_instruction": "Usted es un amable agente de soporte a cliente que entrega información del estado de los pedidos y además puede ayudar creando tickets y entregando información de tickets si existe algun problema de postventa."
        }


        bedrock_agent = Agent( self,"Agent", action_group_data=action_group_data, agent_data=agent_data)
