from twilio.rest import Client


# Your Account SID from twilio.com/console
account_sid = 'ACb3773de653b760cc2ecd341b099f191d'
auth_token = 'ffe383006da1e83eb963e9cb024f858e'

client = Client(account_sid, auth_token)

def text(member, mess, judge):
    print(member, mess)
    final = "Message from Judge " + str(judge) + ": " + str(mess)

    message = client.messages.create(
        to=(str(member)),
        from_="+18552311082",
        body=final)

    print(message.sid)
