# Stock Checker

## Packages
`pip3 install twilio`

## Configuration

### Parameter Store
For each stock that should be checked, create a configuration in Parameter Store at `/prod/stocks` with the name of the stock as the name of the parameter, and the following info as the value:
```
{
   "symbol":"AAPL",
   "price_lowerbound":99,
   "price_upperbound":300,
   "volume_upperbound":1000000000,
   "active": true,
   "recipients":[
      "+15551234567"
   ]
}
```

#### Descriptions
- `symbol` = the ticker symbol of the stock
- `price_lowerbound` = if the current value of the stock is below this value, a message will be sent
- `price_upperbound` = if the current value of the stock is above this value, a message will be sent
- `volume_upperbound` = if the daily volume is above this value, a message will be sent
- 'active' = (true | false) if the stock is currently being watched
- `recipients` = a list of phone numbers which will receive alerts for the stock


### Environment Variables
- `API_KEY` - The api key for the Financial Modeling API (https://financialmodelingprep.com/developer/docs/)
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`

## Deployment
```
cd package
zip -r ../stock-checker.zip .
cd ..
zip -g stock-checker.zip stock-checker.py
aws lambda update-function-code --function-name stockChecker --zip-file fileb://stock-checker.zip
```
