#Import the necessary libraries
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup
import bushandler
import getTime
import checkbusstop

# This function will handle messages with 'chat' flavor, then replies accordingly
def on_chat_message(msg):

        # Gets the headline information of the message
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)


        # Filtering the messages, terminate if incoming message is not text
    if content_type != 'text':
        return

        # Initialize the command variable
    command = msg['text'].lower()


        # Prompt the user to input a bus stop code
    if command == '/start':
        bot.sendMessage(chat_id, "Hello there! Please insert your preferred 5-digit bus stop code"
                                " (e.g: 83139)")


        # Process the bus stop code input
    elif command.isdigit():
        buttons = []
        busstopcode = command

            # Check if the bus stop code entered is a valid 5-digit code. Returns a warning message if not properly entered
        if len(command)!=5 :
            bot.sendMessage(chat_id, 'Sorry, this is not a valid bus stop code.\n'
                                     'Please re-enter a 5-digit bus stop code')


            # Proceed to process the input
        else :

                # Calling a function to check if the input bus stop code is on the list
            if checkbusstop.checkbusstop(busstopcode):
                    # Get a list of services serving a bus stop
                serviceNums = bushandler.getServiceNums(busstopcode)

                    # Check if a serviceNums is a null list -- meaning there's no service available around that time
                if not serviceNums:
                    bot.sendMessage(chat_id, 'Sorry, there is no bus that is servicing this particular bus stop this time around\n'
                                             'Please try again in a couple of moments')
                    # Proceed to process the input
                else:
                        # Iterating through a list of service no
                    for serviceNo in serviceNums:
                            # appends a service number (of dictionary object type) to the button list
                        buttons.append([dict(text=serviceNo, callback_data=serviceNo+busstopcode)])

                    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

                    bot.sendMessage(chat_id, 'You have inputted bus stop code: ' + command + '\nHere we have a list of bus services:', reply_markup=markup)


                # If bus stop code is not found within our database
            else:
                    # - Return an error message
                bot.sendMessage(chat_id, 'Sorry! There is no such bus stop code in our database,\n'
                                         'You might have mistyped your bus stop code. Please try again')
# This function handles message with "callback_query" flavor, then replies accordingly
def on_callback_query(msg):
        # Gets the headline information of the message
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)

        # If the callback_data consists of digit
        # -- that is the concatenation of <SERVICE NO> and <BUS STOP CODE>
        # Replies accordingly
    if data.isdigit():
            #Extracts the bus stop code and service number from the numeric string
        busstopcode = data[-5:]

        serviceNo = data[0:-5]

            #Calls a function that return:
            #InfoLists -- a list of ready to be displayed information
            #completetime -- a list of time with data, complete with the date to be inputted to getTime.stringTime()
        InfoList, completeTime = bushandler.getOneArrival(busstopcode, serviceNo)

            # Formats bus-arrival-time message
        bot.sendMessage(from_id,
                        '<b>ESTIMATED ARRIVAL TIME</b>\n'
                        'Here are the estimated bus arrival times\nfor bus ' + serviceNo + ': \n\n'
                        '🚌 First Bus      \t\t: ' + getTime.stringTime(completeTime[0]) + '\t--\t' + str(InfoList[1]) + "\n"
                        '🚌 Second Bus \t\t: ' + getTime.stringTime(completeTime[1]) + '\t--\t' + str(InfoList[2])+ "\n"
                        '🚌 Third Bus     \t: ' + getTime.stringTime(completeTime[2]) + '\t--\t' + str(InfoList[3]) + "\n\n"
                        'Operator \t\t:\t' + str(InfoList[0]) + '\n\n'
                                           '👍👍 HAVE A NICE TRAVEL 👍👍',
                        'HTML'
                        )

    #Hard-code our token into the program
TOKEN = '471247568:AAFxc95gec9U0QNi0MYPKppZY548JRSDObE'
    #Runs the bot via the API
bot = telepot.Bot(TOKEN)

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

# Keep the program running
while 1:
    time.sleep(10)

