# Stock Checker

## Installation
Install Twilio package
`pip3 install twilio`

## Environment Variables
- `API_KEY` - The api key for the Financial Modeling API (https://financialmodelingprep.com/developer/docs/)
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`

## Deployment
- `cd package`
- `zip -r ../stock-checker.zip .`
- `cd ..`
- `zip -g stock-checker.zip stock-checker.py`
- `aws lambda update-function-code --function-name stockChecker --zip-file fileb://stock-checker.zip`
