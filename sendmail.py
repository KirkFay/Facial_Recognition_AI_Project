# This python file will be used in order to send mail when an
# unrecognized face is detected
import os
import email
import smtplib
from datetime import datetime
from requests import get
import geoip2.database
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send():
    #Get the location based on ip
    ip = get('https://api.ipify.org').text
    reader = geoip2.database.Reader('./GeoLite2-City_20191203/GeoLite2-City.mmdb')
    response = reader.city(ip)
    #Location Data
    city_name = response.city.name
    country_name = response.country.name
    location_lat = response.location.latitude
    location_long = response.location.longitude
    now = datetime.now()
    #Get the date and time of detection
    currentTime = now.strftime("%D at %H:%M:%S")
    #Email Information
    admin_email = ""
    #NOTE: Dr. Yu, if you would like this information to try it out, please let us know.
    # We took it out of our code for security reasons.
    admin_password = ""
    receiver_email = ""
    message = MIMEMultipart("alternative")
    message["Subject"] = "Intuder Detected"
    message["From"] = admin_email
    message["To"] = receiver_email
    img_data = open("intruder_img.jpg", 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename("./intruder_img.jpg"))
    # Create the plain-text and HTML version of your message
    text = """\
     Unverified user has been found at location!
     Please take appropriate action.
     """
    html = """\
    <html>
    <body>
        <h1><u>EVENT DETAILS</u></h1>
        <p> <b>Unknown User Has Been Detected At: </b> %s , %s <br>
            <b>Time Of Detection: </b> %s <br>
            <b>GPS Coordinate Of Location: </b> %s , %s <br>
            <b>Picture of intruder has been attached to this email.</b> <br>
            <b>We urge you to take any appropriate action needed.</b>
            <hr>
            <br>
            <a href="https://github.com/KirkFay/Facial_Recognition_AI_Project">View Source Code</a>
            <br>
        </p>
    </body>
    </html>
    """  % (city_name, country_name,currentTime, location_lat, location_long)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    message.attach(image)

    try:
        #Create an encrypted smtp server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(admin_email, admin_password)
        server.sendmail(admin_email, receiver_email, message.as_string())
        server.close()
        return ('Email sent successfully!')
    except:
        return ('Something went wrong...')
