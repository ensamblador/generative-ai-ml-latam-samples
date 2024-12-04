
# Call Center AI Agent

## Overview
This project demonstrates how to build and deploy an AI-powered Call Center Agent that can handle customer inquiries using natural language interactions. The agent leverages Amazon Bedrock and Lambda functions with action groups to provide intelligent responses to customer questions about their orders and related concerns.

## What is a Call Center AI Agent?
A Call Center AI Agent is an AI-powered application that enables customers to interact naturally with an automated system to resolve their inquiries. It can:
- Look up order information using order numbers and customer identification
- Handle customer support queries
- Create support tickets when necessary
- Maintain context throughout the conversation
- Escalate complex cases to human agents

## Architecture
The solution uses several AWS services:
- Amazon Lex V2 for natural language understanding
- AWS Lambda for business logic and integration
- Amazon Bedrock for advanced language model capabilities
- DynamoDB for storing chat history and session management
- CloudWatch for logging and monitoring

## Prerequisites

### CDK Setup
1. Install the AWS CDK CLI
2. Configure AWS credentials
3. Install project dependencies:
```bash
npm install -g aws-cdk
python -m pip install -r requirements.txt
```

### Model Access
Ensure you have access to the required Amazon Bedrock models in your AWS account.

## Deployment

1. Clone the repository
2. Navigate to the project directory
3. Deploy the CDK stack:
```bash
cdk deploy
```

## Features
The Call Center AI Agent includes:
- Natural language order lookup
- Customer support ticket creation
- Conversation history tracking
- Intelligent response generation using LLMs
- Automated escalation to human agents when needed

## Testing your agent
1. Access the deployed bot through the AWS Console
2. Start a conversation by providing your order number and RUT (Chilean ID)
3. Ask questions about your order or request support
4. Test different scenarios like:
   - Order status inquiries
   - Support ticket creation
   - Complex queries requiring escalation

## Security
This implementation includes:
- IAM roles and permissions for secure service access
- Data privacy controls
- Session management
- Secure handling of customer information

## Cost Considerations
The solution uses pay-as-you-go AWS services:
- Lex V2 charges per request
- Lambda invocation and compute charges
- Bedrock model inference costs
- DynamoDB storage and request charges

## Cleanup
To remove the deployed resources:
```bash
cdk destroy
```

## Where to go from here?
Consider extending the solution with:
- Additional language support
- More sophisticated dialogue management
- Integration with additional backend systems
- Enhanced analytics and reporting
- Advanced error handling and recovery
