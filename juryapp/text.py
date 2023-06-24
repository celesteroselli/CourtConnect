from twilio.rest import Client


# Your Account SID from twilio.com/console
account_sid = "ACb3773de653b760cc2ecd341b099f191d"
# Your Auth Token from twilio.com/console
auth_token  = "0b4761ca7b1dee46050e83fdb82ae9b6"

client = Client(account_sid, auth_token)

def text(member, message):
    print(member, message)

    message = client.messages.create(
        to=("+1" + str(member)),
        from_="+18552311082",
        body=message)

    print(message.sid)