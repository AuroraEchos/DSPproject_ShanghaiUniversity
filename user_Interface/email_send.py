import yagmail

def send_email(user_email,user_feedback):
    try:
        yag=yagmail.SMTP(user='',password='',host='')
        yag.send(to=[''],subject=user_email,contents=user_feedback)
        print('Email send success')
    except:
        print('Email send fail')