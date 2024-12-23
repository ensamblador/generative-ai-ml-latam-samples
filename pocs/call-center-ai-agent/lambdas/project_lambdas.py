from aws_cdk import aws_lambda, Duration
from constructs import Construct

LAMBDA_TIMEOUT= 300

BASE_LAMBDA_CONFIG = dict (
    timeout=Duration.seconds(LAMBDA_TIMEOUT),       
    memory_size=256,
    architecture=aws_lambda.Architecture.ARM_64,
    runtime=aws_lambda.Runtime.PYTHON_3_12,
    tracing= aws_lambda.Tracing.ACTIVE)


class Lambdas(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        COMMON_LAMBDA_CONF = dict(environment= {},**BASE_LAMBDA_CONFIG)

        self.fulfillment = aws_lambda.Function(
            self, "LexFullfillment", handler="lambda_function.lambda_handler",
            code = aws_lambda.Code.from_asset("./lambdas/code/fulfillment"), **COMMON_LAMBDA_CONF)
    

