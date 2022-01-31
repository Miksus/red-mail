from .sender import EmailSender

gmail = EmailSender(
    host="smtp.gmail.com",
    port=587,
)

outlook = EmailSender(
    host='smtp.office365.com',
    port=587,
)

def send_email(*args, host:str, port:int, user_name:str=None, password:str=None, **kwargs):
    """Send email

    Parameters
    ----------
    host : str
        Address of the SMTP host
    port : int
        Port of the SMTP server
    user_name : str
        User to send the email with
    password : str
        Password of the user to send the email with
    **kwargs : dict
        See redmail.EmailSender.send
    """
    sender = EmailSender(
        host=host, 
        port=port, 
        user_name=user_name,
        password=password
    )
    return sender.send(*args, **kwargs)