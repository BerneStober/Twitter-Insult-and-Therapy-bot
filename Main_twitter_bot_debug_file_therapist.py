import tweepy
import time
import sys
import inspect
import eliza
from datetime import datetime

from config import create_api
import random

#not using logging anymore
# use print to console for debugging
# un comment these lines if you want to use logging
#import logging
#logging.basicConfig(level=logging.INFO, filename='autoreply_alt_newer.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#logger = logging.getLogger()

# set Debug_sleep for stepthru to 5
# set to 75 for execution

# use following line if you want debug p[rints saved to file
#f = open("Bot_debug_prints_new.txt", "a", encoding='utf-8')

# for directing debug output to console
f = sys.stdout 

therapist = eliza.Eliza()
Debug_sleep = 76
Recent_rands = []

# put your screen name here
screen_name = 'XXXXXXXXXXX'
# the following are binary values which are used to control execution flow
StreamLoop = 1
OuterLoop = 1
Therapist = 0
ExitBot = 'no'

# this just restricts search on older tweets -- this is a tweet id
# you will need to update this based on your own tweet id numbers
since_id = 1280642194953682949

# make sure your Twitter bot credentials are stored in create_api
api = create_api()
# find latest tweet_id
new_since_id = since_id
 
# find latest tweet by the user and set since_id there
tweets = api.user_timeline(screen_name, count = 1)
for tweet in tweets:    
    new_since_id = max(tweet.id, new_since_id)
    print("Current Tweet: ", tweet.text, file=f)
   
since_id = new_since_id 
print("Since_id at start", since_id, file=f)
print ('\n', file=f)
#logger.info("Since_id at start:", since_id)

# these are Joe Biden like insults captured from the Biden Insult bot
# when it was active
# can be replaced  
def new_insult_bot(input):
    switcher = {
       0: "You're hootin' at the wrong owl, you nursery-rhymin' can o' beans",
       1: "Keep it in your hat, you ol' dribble-mouthed milk licker",
       2: "Go candy a yam, you two-faced spit-licker",
       3: "You're all strawberry and no preserves, ya foghorn-blowin' trolley jumper",
       4: "You woke the rooster this time, ya lemon-squeezin' Chicken Little",
       5: "Tell it to the judge, you liver-spotted deuce of diamonds",
       6: "Go on, git, you stink-heinied unfinished rocking chair",
       7: "Everybody in the neighborhood knows youse a coupon-clippin' Mallo Cup",
       8: "You jackknifed the wrong turnip truck, ya diesel-pumpin' pony-soldier",
       9: "You just hitched your dinghy to the wrong river boat, ya gum-swallowin' flutter butt",
       10: "Cool your heels, you pie-faced hobby horse", 
       11: "Go hike the pike, you yellow snow eatin' pony-soldier",
       12: "Shut your beak, you scrumble-brained hippie armpit",
       13: "You are a hairy lickspittle chicken-leg rubbing cretin with square eyes!",
    }
    
    return switcher.get(input, "You are a very sad example of non-human")

# this is part of cdode which randomizes insults while trying to avoid repeats
def insult_bot(input):
    global Recent_rands
    randnum = random.randint(0,13)
    if (randnum) not in Recent_rands:
        insult = new_insult_bot(randnum)
        # append randnum onto list 
        Recent_rands.append(randnum)
    else:
        insult = new_insult_bot(randnum) + ", " + input 
    #logger.info(randnum, insult)
    
    
    return insult

# this is the insult and block code, 4 insults then a block
def blocking_insults(api, since_id, insulter, block, block_counter):
    #global InnerLoop, OuterLoop
    #logger.info("Retrieving mentions")
    print("Starting insults with blocks", file=f)
    print ('\n', file=f)
    new_since_id = since_id
    while block_counter < 4:
        #new_since_id = max(tweet.id, new_since_id)
        #logger.info(f"Since_id:", new_since_id)
        #logger.info(f"Current tweet:", tweet.text)
        print("Answering to " + insulter, file=f)
        print ('\n', file=f)
        insult = insult_bot(" " + insulter)
        # unblock
        api.destroy_block(insulter)
        time.sleep(2)       
        print(insulter + " unblocked", file=f)
        print ('\n', file=f)
        # insult
        api.update_status(status=insulter + " " + insult, in_reply_to_status_id=tweet.id,)
        #capture tweet.id of insult here
        tweets = api.user_timeline(screen_name, count = 1)
        for tweet in tweets:    
            insult.id = max(tweet.id, new_since_id)
            print("Current insult: ", tweet.text, file=f)
            print("insult.id: ", insult.id, file=f)
        
        time.sleep(2)
            # reblock
        api.create_block(insulter)
        print(insulter + " blocked", file=f)
        print ('\n', file=f)
        #logger.info(f"Answered to {tweet.user.name}")
        print("Answered to " + insulter, file=f)
        print ('\n', file=f)
        
        # pause 45 seconds for insulted to read insult
        time.sleep(Debug_sleep/4*3)
        # delete insult
        api.destroy_status(insult.id)
        print("deleted insult", insult.id, file=f)

        block_counter = block_counter + 1
        time.sleep(Debug_sleep/2)

    block = 0
    block_counter = 0 
    InnerLoop = 0
    OuterLoop = 1
    return 


def check_mentions(api, keywords, since_id, insulter, Therapist):
    #logger.info("Retrieving mentions")
    # add therapist code here!
    print("Retrieving mentions", file=f)
    print ('\n', file=f)
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        #logger.info(f"Since_id:", new_since_id)
        #logger.info(f"Current tweet:", tweet.text)
        time.sleep(1)
        print("Since_id:", new_since_id, file=f)
        print("Current Tweet: ", tweet.text, file=f)
        if tweet.in_reply_to_status_id is not None:
       #     continue
       #if any(keyword in tweet.text for keyword in keywords) and (name in tweet.text):
            #logger.info(f"Answering to {tweet.user.name}")
            print("Answering to " + tweet.user.name, file=f)
            print ('\n', file=f)
            #if not tweet.user.following:
            #    tweet.user.follow()
            if Therapist == 0: 
                insult = insult_bot(" " + insulter)
                # insulter problem
                api.update_status(
                    status=insulter + " " + insult,
                    in_reply_to_status_id=tweet.id,)
            elif Therapist == 1:
                # strip @screenname from beginning of tweet.text
                response = tweet.text.split(' ', maxsplit = 1)[1]
                reply = therapist.respond(response)
                api.update_status(
                    status=insulter + " " + reply,
                    in_reply_to_status_id=tweet.id,)

            #logger.info(f"Answered to {tweet.user.name}")
            print("Answered to "+ tweet.user.name, file=f)
            print ('\n', file=f)
    return new_since_id

    
def InnerLoops(since_id, InnerLoop, insulter, Therapist):    
    # now infinite loop until other user gives up, keep insulting 
   #global Therapist, InnerLoop
   while InnerLoop:
        #logger.info("In inner loop")
        print("In inner loop", file=f)
        
        # this list is not used in this version
        notnicewords = ["idiot", "Idiot", "stupid", "Stupid", "Trumptard", "insult", "fuck", "fck", "FU", "dick", "Dick"]
        #logger.info("Now do check mentions and insult")
        print("Now do check mentions and insult or therapy", file=f)
        print ('\n', file=f)
        since_id = check_mentions(api, notnicewords , since_id, insulter, Therapist)
        tweets = api.user_timeline(screen_name, since_id=since_id, count = 5)
        for tweet in tweets:
            print (tweet.text.lower(), file=f)
            # these are the code words used to stop the bot or change its behavior
            if ((("stop insulting") in tweet.text.lower()) 
            or (("stop bot") in tweet.text.lower()) 
            or (("stop therapy") in tweet.text.lower())):
                InnerLoop = 0
                Therapist = 0 
                #logger.info(f"found stop insulting or stop bot in BKS tweet to {tweet.user.name}")
                print("found stop insulting or stop bot or stop therapy in BKS tweet", file=f)
                break
            else:
                InnerLoop = 1
        #logger.info("Waiting... in inner loop")
        print("Waiting .... in inner loop", file=f)
        print (InnerLoop, " ", Therapist, file=f)
        print ('\n', file=f)
        time.sleep(5)
        
 
def Get_Time_Since_Last_Tweet():
     tweets = api.user_timeline(screen_name, count = 1)
     for tweet in tweets:
            #logger.info(tweet.text)
            print ('In Get_Time_Since_Last_Tweet', file=f)
            print(tweet.text.lower(), file=f) 
            print(tweet.created_at, file=f)
            dumstr = str(tweet.created_at)
            print (dumstr, file=f)
            Time_of_Last_Tweet = datetime.strptime(dumstr, "%Y-%m-%d %H:%M:%S")
            print("Date and Time of Last tweet =", Time_of_Last_Tweet, file=f)
            Time_Now = datetime.now()
            print (Time_Now, Time_of_Last_Tweet, file=f)
            Time_Difference = Time_Now - Time_of_Last_Tweet
            Time_Difference_secs = Time_Difference.total_seconds()
            print (Time_Difference_secs, file=f)
            #tweet time is based on GMT have to correct for six hours. 
            # may have to change this for EST when day light ends
            Time_Difference_mins = Time_Difference_secs/60 + 240
            print ('\n', file=f)
            return Time_Difference_mins

def OuterLoops():    
    global InnerLoop, OuterLoop, ExitBot
    while OuterLoop:
        # check last five tweets for key phrase
        #logger.info("In top of outer loop, getting my tweets")
        print("In top of outer loop, getting my tweets", file=f)
        print ('\n', file=f)
        tweets = api.user_timeline(screen_name, count = 5)
        
        time.sleep(2)
        for tweet in tweets:
            #logger.info(tweet.text)
            print(tweet.text.lower(), file=f) 
            print(tweet.created_at, file=f)
            print(tweet.id, file=f)
            print ('\n', file=f)
            
            # if key phrase found execute this code
            # this is the code phrase to start insulting
            if ('insult me') in tweet.text.lower():
                status_id = tweet.in_reply_to_status_id
            # got to make sure this works to extract the true insulter especially is a multi thread
                insulter = tweet.text.rsplit(' ')[0]
                #logger.info("Found trigger, Start insulting:", insulter)
                
                print("Found trigger, Start insulting:", insulter, file=f)
                # if the following is found in addition to insult me, it turns on the insult and block logic
                if ('!@#$' in tweet.text) or ('@#$&' in tweet.text):
                    #added ipad character string
                    # turn on blocking 
                    block = 1
                    block_counter = 0 
                    print("Found blocking trigger", file=f)
                    print ('\n', file=f)
                else:
                    block = 0
                    print("No blocking trigger", file=f)
                    print ('\n', file=f)
                
                # make sure we delete the trigger tweets so they don't cause problems later
                api.destroy_status(tweet.id)
                insult = insult_bot(" " + insulter)
                api.update_status(status=insulter + " " + insult,
                in_reply_to_status_id=tweet.id,)
                # now if blcoking do block and increment block counter
                # put a delay here!
                time.sleep(Debug_sleep)
                if (block == 1) and ('@' in insulter):
                    api.create_block(insulter)
                    block_counter = 1
                since_id=status_id   
                InnerLoop = 1
                OuterLoop = 1
                #logger.info("go to innerloop to keep insulting until stopped")
                print("go to innerloop to keep insulting until stopped", file=f)
                print ('\n', file=f)
                if block != 1:
                    InnerLoops(since_id, InnerLoop, insulter)
                elif (block ==1) and ('@' in insulter):
                    blocking_insults(api, since_id, insulter, block, block_counter)
                    return 
                else:
                    return
            
            # following are the code words to invoke the therapy option
            elif ('need a therapist') in tweet.text.lower():
                print("trigger to start eliza therapy found", file=f)
                print ('\n', file=f)
                status_id = tweet.in_reply_to_status_id
                # got to make sure this works to extract the true insulter especially is a multi thread
                patient = tweet.text.rsplit(' ')[0]
                #logger.info("Found trigger, Start insulting:", insulter)
                api.destroy_status(tweet.id)
                reply = therapist.respond("I need help.")
                api.update_status(status=patient + " " + reply,
                in_reply_to_status_id=tweet.id,)
                since_id=status_id 
                OuterLoop = 1
                InnerLoop = 1
                Therapist = 1
                Recent_rands = []
                print (OuterLoop, " ", StreamLoop, " ", ExitBot, " ", Therapist, file=f)
                print ('\n', file=f)
                InnerLoops(since_id, InnerLoop, patient, Therapist)
                time.sleep(2)
                return 

            elif ('stop insulting') in tweet.text.lower():
                print("trigger to stop insulting found, stop insulting", file=f)
                print ('\n', file=f)
                # make sure we delete the trigger tweets so they don't cause problems later
                api.destroy_status(tweet.id)
                insulter = None
                OuterLoop = 1
                InnerLoop = 0
                Therapist = 0
                Recent_rands = []
                print (OuterLoop, " ", StreamLoop, " ", ExitBot, file=f)
                print ('\n', file=f)
                time.sleep(Debug_sleep)
                return 
            
            elif ('stop therapy') in tweet.text.lower():
                print("trigger to stop therapy found", file=f)
                print ('\n', file=f)
                # make sure we delete the trigger tweets so they don't cause problems later
                api.destroy_status(tweet.id)
                insulter = None
                OuterLoop = 1
                InnerLoop = 0
                Therapist = 0
                Recent_rands = []
                print (OuterLoop, " ", StreamLoop, " ", ExitBot, " ", Therapist, file=f)
                print ('\n', file=f)
                time.sleep(Debug_sleep)
                return 

            elif ('stop bot') in tweet.text.lower():
                insulter = None
                #logger.info("trigger to stop the bot found, exit")
                print("trigger to stop the bot found, exit", file=f)
                print ('\n', file=f)
                # make sure we delete the trigger tweets so they don't cause problems later
                api.destroy_status(tweet.id)
                OuterLoop = 0
                ExitBot = 'yes'
                Recent_rands = []
                print (OuterLoop, " ", StreamLoop, " ", ExitBot, " ", Therapist, file=f)
                print ('\n', file=f)
                return OuterLoop, ExitBot
            
            else:
                time.sleep(2)
                

        print ('at bottom of outer loop code', file=f)
        print ('\n', file=f)
        time.sleep(Debug_sleep)
        Time_Diff_min = Get_Time_Since_Last_Tweet()
        # if time since last tweet greater than 30 min go back to streaming checks
        #change this to thirty after debugged
        print ('Time since last tweet(min): ',Time_Diff_min, file=f)
        print ('\n', file=f)
        if (Time_Diff_min > 30):
            OuterLoop = 0
            #return OuterLoop, ExitBot
        #go back to streaming/sleeping mode
        print (OuterLoop, " ", StreamLoop, " ", ExitBot, file=f)
        print ('\n', file=f)
    return OuterLoop, ExitBot

# this code allows the bot to just sit around sort of idling until the user
# is actively tweeting
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global InnerLoop, OuterLoop, ExitBot, StreamLoop    
        if  status.user.screen_name.lower() == 'bernestober':
            print ('TWEET:', status.text.encode('UTF-8'), file=f)
            #print ('FOLLOWERS:', status.user.followers_count)
            print (time.ctime(), file=f)
            #myStream.disconnect()
            #try deleting stream object instead
            #del myStream
            #print('Streaming disconnected')
            #try this to avoid error
            #myStream.listener.on_data() = False
            print ('\n', file=f)
            OuterLoops()
                #if OuterLoop == 0: 
                #    return False
                #else:
                    #redo streaming
                    #myStream.running = True
                    #myStream.listener.on_data = True
                #    myStream.filter(follow=["346905146"])
            print('Exited OuterLoop in main', file=f)
            if (ExitBot) == 'yes':
                StreamLoop = 0
            #returning false should turn off streaming
            print (OuterLoop, " ", StreamLoop, " ", ExitBot, file=f)
            print ('\n', file=f)
            return False


    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.

#My Twitter user id

while StreamLoop:
    try:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())
        #myStream.filter(follow=["346905146"], is_async=True)
        #reset OuterLoop for next tweet. 
        OuterLoop = 1
        print ('Start streaming checks for tweets', file=f)
        print (OuterLoop, " ", StreamLoop, " ", ExitBot, file=f)
        print ('\n', file=f)
        myStream.filter(follow=["346905146"])
    except:
        print('twitter stream dropped, redoing', file=f)
        print('\n', file=f)
        time.sleep(Debug_sleep/2)
        continue

print('Ended streaming', file=f)
f.close()