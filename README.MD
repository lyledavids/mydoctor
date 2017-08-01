
# Inspiration
What if I have my own  personal assistant who will be able to search all available practitioners, check their availability, make appointments for me, set reminders for due appointments and GP re-calls. The Goal is to have a centralized bot platform which connects all available practices (GP Clinics), so clients/patients will be able to choose any preferred practitioners from any clinics. 

# What it does

MyDoctor is a revolutionized, interactive and user friendly chat bot which interacts with registered practitioners and GP Clinics for  booking, scheduling and managing medical appointments. It will also  be your personal assistant to remind  medical appointments.

# How we built it

* Process user conversations using intents and contexts especially designed and trained for **MyDoctor** .
* Based on conversational analysis, bot will perform required actions via integrated health care practitioners management system API. (eg. adding patients, searching practitioners, checking doctor availability, making bookings, modifying bookings,etc)
* Details of Integrated health care practices and user information are stored in our database.
* Bot works with user in full conversational mode. 
* Required conversation contexts are preserved throughout the conversation for better and flawless user experience. for example, if requested time slot is unavailable, user will be asked to choose he available time slots while remembering the details from previous conversation, such as date and requested practitioner name.

Following technology used for developing this system
* api.ai
* mlab ( Mongo DB)
* heroku
* Cliniko - Healthcare practice management software


# Challenges we ran into
* Implementing flaw less conversational flows with diverse contexts to serve different user requests.
* Providing better user experience and meeting user expectation through conversational interface
* formation of a centralized practitioners/practices database which keeps updated and accurate data about practices with various practice management software vendors. 


# Accomplishments that we're proud of
* Fully functional prototype model is available
* Successfully partnered and integrated with Australia's most preferred practice management software (Cliniko)


# How to use
* You can search **MyDoctor** or **MyDoctor@sparkbot.io** in Cisco Spark app.
* Simple **'hi'** will start the one to one conversation with bot.
*  If you are a first time user, **MyDoctor** bot will walk you through few simple questions to on board you.
* Start typing **"I need to book an appointment with Dr Pat"** , bot will ask you for missing details (date & time).
* If required date and time is available, Bot will make booking and give you the booking details.
* If required date and time is unavailable, Bot will give you available slots so you can choose.

# What's next for MyDoctor
* Integrate with other practice management software (Medical director, Pracsoft, etc)
* Search practitioners based on the services they offer (Osteopathy, Physiotherapy, Psychology, Massage, Podiatry, etc.)
* Integrating Cisco Tropo for SMS based authorization for user on boarding and appointment bookings



