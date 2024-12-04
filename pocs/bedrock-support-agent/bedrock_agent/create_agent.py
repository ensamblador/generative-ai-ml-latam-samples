from aws_cdk import RemovalPolicy, aws_bedrock as bedrock
from constructs import Construct

class CreateAgent(Construct):
    def __init__(self, scope: Construct, construct_id: str, agent_data, agent_role, ag_property=None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        agent_name = agent_data.get("agent_name") if agent_data.get("agent_name") else "simple-agent-cdk"
        agent_description = agent_data.get("description") if agent_data.get("description") else "Sample Agent"
        agent_instruction = agent_data.get("agent_instruction") if agent_data.get("agent_instruction") else "You are a helpful AI Agent"
        foundation_model = agent_data.get("foundation_model") if agent_data.get("foundation_model") else "anthropic.claude-3-haiku-20240307-v1:0"

        agent_kwags = dict(
            agent_name=agent_name,
            description=agent_description,
            auto_prepare=True,
            idle_session_ttl_in_seconds=600,
            skip_resource_in_use_check_on_delete=False,
            test_alias_tags={"test_alias_tags_key": "testAliasTags"},
            agent_resource_role_arn=agent_role.arn,
            instruction=agent_instruction,
            foundation_model=foundation_model
        )
        
        if ag_property: agent_kwags["action_groups"] = ag_property


        self.cfn_agent = bedrock.CfnAgent( self,"Agent", **agent_kwags)

        self.cfn_agent.apply_removal_policy(RemovalPolicy.DESTROY)
