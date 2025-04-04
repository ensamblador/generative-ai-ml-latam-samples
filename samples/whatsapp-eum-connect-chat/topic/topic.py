from aws_cdk import (
    aws_sns as sns,
    aws_ssm as ssm,
    aws_sns_subscriptions as subs,
    aws_iam as iam,
)

from constructs import Construct


class Topic(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        notification_email=None,
        lambda_function=None,
        filter_policy=None,
        filter_policy_with_message_body=None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.topic = sns.Topic(self, "Topic")

        if lambda_function:
            self.topic.add_subscription(subs.LambdaSubscription(lambda_function))

    def add_lambda_subscription(
        self, lambda_function, filter_policy=None, filter_policy_with_message_body=None
    ):
        self.topic.add_subscription(subs.LambdaSubscription(lambda_function,
            filter_policy=filter_policy,
            filter_policy_with_message_body=filter_policy_with_message_body))

    def allow_principal(self, service_principal):
        self.topic.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.ServicePrincipal(service_principal)],
                actions=["sns:Publish"],
                resources=[self.topic.topic_arn],
            )
        )
