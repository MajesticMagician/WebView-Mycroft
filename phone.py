# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC6f537500aecd24189b7740b805345b37'
auth_token = 'df3a7e92c3cb146764f53895ea13d910'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+17197289392',
                        from_='+19254526914'
                    )

print(call.sid)