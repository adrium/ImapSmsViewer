# Receive SMS

SMS Viewer with IMAP Backend.
Used with an Android phone with [SMS Backup+](https://play.google.com/store/apps/details?id=com.zegoggles.smssync) or [SMS Gate](https://f-droid.org/en/packages/com.github.axet.smsgate/).
Running on the AWS API Gateway and AWS Lambda.

## Deployment

1. Deploy files to [Lambda](https://console.aws.amazon.com/lambda) as Python _ReceiveSms_
2. Edit `config/numbers.local.json`
3. Edit `swagger.yml` and replace the `REGION_APIGW` and `ARN_LAMBDA` strings
4. Deploy `swagger.yml` to [AWS API Gateway](https://console.aws.amazon.com/apigateway) by importing a REST API
5. Edit `/{file+} - GET - Integration Request` and reselect the lambda function. It will give the necessary invoke permissions
6. Deploy API
