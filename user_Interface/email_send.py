import yagmail

def send_email(user_email,user_feedback):
    try:
        yag=yagmail.SMTP(user='2726433780@qq.com',password='wycjjftbtgqydffe',host='smtp.qq.com')
        yag.send(to=['3111013462@qq.com'],subject=user_email,contents=user_feedback)
        print('Email send success')
    except:
        print('Email send fail')