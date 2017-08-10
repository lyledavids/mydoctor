
# Inspiration
What if we have our own  personal assistant who will be able to search all available practitioners, check their availability, make appointments for me, set reminders for due appointments and GP re-calls. The Goal is to have a centralized bot platform which connects all available practices (GP Clinics), so clients/patients will be able to choose any preferred practitioners from any clinics. 

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

# Conversational Work flow

* **Welcome** - New & un-registered users will be greeted with standard welcome message with the details of the services bot can offer and they will be prompted if they wish to proceed with on-boarding process
* **user.on-boarding** - If a client said 'yes' to on boarding option, MyDoctor will start to collect few basic user information such as Firstname, lastname, date of birth, and address. Bot will skip asking the information which is known to it. for example, if fisrtname or lastname is available from Cisco Spark, Bot will use available information and gather only missing details.
* **user.store** - Gathered user details will be stored in database
* **greet.personal**-User will be identified and greeted personally after on boarding process is completed.
* **Find.gp** - User can search available practitioners registered with myDoctor Bot platform
* **book.Doctor** - If user's intention was to book a doctor, Bot will ask date, time details.
* **book.confirm(user)** - user will be asked if he/she wants to confirm the appointment booking.
* **patient.create** - If user confirms the booking, if it is a first time patient for the practice, gathered patient details will be inserted into practice management system. If booking request comes from an existing patient, this step will be skipped.
* **Appointment.create** - If user confirms the booking, appointment will be created in practice management software.
* **Appointment.alternate** - If user requested slot is not available, bot will suggest available slots for specific doctor.


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
* Type **"find a gp"** to find registered practitioners. For demo purposes MyDoctor will provide a list of doctors from a single practice.
* Start typing **"I need to book an appointment with Dr Pat"** , bot will ask you for missing details (date & time).
* If required date and time is available, Bot will make booking and give you the booking details.
* If required date and time is unavailable, Bot will give you available slots so you can choose.

# What's next for MyDoctor
* Integrate with other practice management software (Medical director, Pracsoft, etc)
* Search practitioners based on the services they offer (Osteopathy, Physiotherapy, Psychology, Massage, Podiatry, etc.)
* Integrating Cisco Tropo for SMS based authorization for user on boarding and appointment bookings



