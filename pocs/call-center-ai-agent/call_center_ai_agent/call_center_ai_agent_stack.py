from aws_cdk import Stack, aws_iam as iam, aws_connect as connect
from constructs import Construct
from aws_cdk.aws_s3_assets import Asset
from bots import LexBotV2
from lambdas import Lambdas
from databases import Tables


bot_locale = "es_419"
bot_name = "ai-agent"
alias_name = None
amazon_connect_instance_id = "f5dbbb06-46e7-4435-beab-3b3303074765"


class CallCenterAiAgentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stk = Stack.of(self)
        region = stk.region
        account_id = stk.account

        Tb = Tables(self, "Tb")
        Fn = Lambdas(self, "Fn")

        Fn.fulfillment.add_environment(
            "CONVERSATION_TABLE_NAME", Tb.conversationHistory.table_name
        )
        Fn.fulfillment.add_environment("ORDER_TABLE_NAME", Tb.pedidos.table_name)
        Fn.fulfillment.add_environment("TICKET_TABLE_NAME", Tb.issues.table_name)

        Fn.get_customer_data.add_environment("ORDER_TABLE_NAME", Tb.pedidos.table_name)

        bot_assets = Asset(self, "Zipped", path="bots/pedido-llm")

        demo_bot = LexBotV2(
            self,
            "AIAgent",
            bot_name=bot_name,
            bot_locale=bot_locale,
            code_hook=Fn.fulfillment,
            alias=alias_name,
            s3_key=bot_assets.s3_object_key,
            s3_bucket=bot_assets.bucket,
        )



        # Add integrations to amazon connect if amazon_connect_instance_id is defined
        if amazon_connect_instance_id:
            instance_arn = f"arn:aws:connect:{region}:{account_id}:instance/{amazon_connect_instance_id}"

            connect.CfnIntegrationAssociation(self, "LambdaGetCustomerDataIntegration",
                instance_id=instance_arn,integration_type="LAMBDA_FUNCTION",
                integration_arn=Fn.get_customer_data.function_arn)
            
            bot_integration_arn = f"arn:aws:lex:{region}:{account_id}:bot-alias/{demo_bot.bot.attr_id}/TSTALIASID"

            connect.CfnIntegrationAssociation(self, "BotIntegrationAIAgent",
            instance_id=instance_arn,
            integration_type="LEX_BOT",
            integration_arn=bot_integration_arn
        )


        # Pemissions

        Fn.fulfillment.add_permission(
            principal=iam.ServicePrincipal(
                "lexv2.amazonaws.com"
            ),  # Allow Lexv2 to invoke this function
            id=f"{bot_name}-invoke",
            action="lambda:InvokeFunction",
            source_arn=f"arn:aws:lex:{Stack.of(self).region}:{Stack.of(self).account}:bot-alias/*",
        )

        Fn.fulfillment.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:Invoke*"],
                resources=[
                    f"arn:aws:bedrock:{region}:{account_id}:agent*",
                    "arn:aws:bedrock:us-east-1::foundation-model/*",
                    "arn:aws:bedrock:us-east-2::foundation-model/*",
                    "arn:aws:bedrock:us-west-2::foundation-model/*",
                    f"arn:aws:bedrock:{region}:{account_id}:inference-profile/*",
                    ]
            )
        )

        Tb.pedidos.grant_read_data(Fn.get_customer_data)
        Tb.pedidos.grant_read_data(Fn.fulfillment)
        Tb.issues.grant_read_write_data(Fn.fulfillment)
        




