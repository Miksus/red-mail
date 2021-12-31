from .sender import EmailSender

gmail = EmailSender(
    server="smtp.gmail.com",
    port=587,
)

def send_email(*args, server:str, port:int, user_name:str, password:str, **kwargs):
    """Send email

    Parameters
    ----------
    server : str
        Address of the SMTP server
    port : int
        Port of the SMTP server
    user_name : str
        User to send the email with
    password : str
        Password of the user to send the email with
    **kwargs : dict
        See redmail.EmailSender.send_email
    """
    sender = EmailSender(
        server=server, 
        port=port, 
        user_name=user_name,
        password=password
    )
    return sender.send_email(*args, **kwargs)