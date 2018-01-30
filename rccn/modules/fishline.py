import sys
sys.path.append("..")
from config import *
import sms
import sqlite3
#States of users 
#'advertiser' = currently advertising 
#'probablyadvertiser' = Waiting for confirmation on advertisement
#'advertisementsent' = Advertisement was sent
#'wantstobuy' = Wants to buy fish
#'doesnotwanttobuy' = Not interested
#'removeme' = Asked to be removed 
#'unsubscribed' = unsubscribed from the app
#'done' 

#To subscribe a user has to send the message 'subscribe [NAME INITIALS]'
#

class fishline:
	def __init__(self):
		self.state = {}
		self.advertisements = {}
		self.lastadvertisement = ''
		self.lastadvertiser = ''
		conn = sqlite3.connect('/home/rhizomatica/fishline.db')
		c = conn.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS advertisers (date datetime, frm text, initials text)")
		c.execute('''CREATE TABLE IF NOT EXISTS allMessages (date datetime, frm text, msg text)''')
		c.execute('''CREATE TABLE If NOT EXISTS userStates (user text, state text)''')
		c.execute("CREATE TABLE IF NOT EXISTS ads (date datetime, frm text, ad text)")
		conn.commit()
		conn.close()	
	def getState(self, sender):
		conn = sqlite3.connect('/home/rhizomatica/fishline.db')
		query = "select state from userStates where user='%s'" %sender
		c = conn.cursor()
		c.execute(query)
		userstate = c.fetchone()
		conn.commit()
		conn.close()

		if userstate is not None:
			print 'user state is not none in get state'
			return userstate[0]
		else:
			print "user state is None"
			return None
	def getAdd(self,sender):
		conn = sqlite3.connect('/home/rhizomatica/fishline.db')
		query = "select ad from ads where frm = '%s'" %(sender)
		c = conn.cursor()
		c.execute(query)
		ad = c.fetchone()
		conn.commit()
		conn.close()
		if ad is not None:
			return ad[0]	
		else:
			return None
	def checkAdvertiser(self,sender):
		conn = sqlite3.connect('/home/rhizomatica/fishline.db')
		query = "select initials from advertisers where frm = '%s'" %(sender)
		c = conn.cursor()
		c.execute(query)
		ad = c.fetchone()
		conn.commit()
		conn.close()
		if ad is not None:
			return True	
		else:
			return False

	def setState(self, sender, state):
		if self.getState(sender)==None:
			query = "insert into userStates values('%s','%s')" %(sender,state);
		else:
			query = "update userStates set state='%s' where user='%s'" %(state,sender)
		conn = sqlite3.connect('/home/rhizomatica/fishline.db')
		c = conn.cursor()
		c.execute(query)
		conn.commit()
		conn.close()		
	def setAdd(self,sender,ad):
		if self.getAdd(sender)==None:
			query="insert into ads values(%d,'%s','%s')" %(time.time(),sender,ad)
		else:
			query="update ads set date=%d,ad='%s' where frm='%s'" %(time.time(),ad,sender)
		conn = sqlite3.connect('/home/rhizomatica/fishline.db')
		c = conn.cursor()
		c.execute(query)
		conn.commit()
		conn.close()
	def receive(self, sender, to, text):
		senderState = self.getState(sender)
		sms_log.info("senderState=%s" %senderState);
		sms_log.info("to=%s" %to);
		if 'subscribe' in text.lower() and to == '20000':
			self.setState(sender,'done');
			self.send(20000,sender,'You are subscribed to fishline')
			query = "Insert into advertisers values (%d,'%s','%s')" %(time.time(),sender,text.split()[-1])
			conn = sqlite3.connect('/home/rhizomatica/fishline.db')
			c=conn.cursor()
			print query
			c.execute(query)
			conn.commit()
			conn.close()
			return
		elif to=='20000' and self.checkAdvertiser(sender) is True:# and senderState!='probablyadvertiser':
			#self.state[sender] = 'probablyadvertiser'
			query = "select initials from advertisers where frm = '%s'" %sender
			conn = sqlite3.connect('/home/rhizomatica/fishline.db')
			c = conn.cursor()
			print query
			c.execute(query)
			initials = c.fetchone()
			initials = initials[0]
			conn.commit()
			conn.close()
			
			#initials = 'TA'
			self.setState(sender,'advertiser')
			#self.lastadvertisement=self.advertisements[sender][-1]
			#self.lastadvertiser = sender
			print initials.upper()
			string = ". If interested reply 'yes %s' " %(initials.upper())
			#self.lastadvertisement=self.getAdd(sender)
			self.lastadvertisement=text
			self.sendbulk('30000',self.lastadvertisement+string)
			return
		elif 'yes ' in text.lower() and to =='30000':
			initials = text.split()[-1]
			query = "select frm from advertisers where initials = '%s'" %(initials)
			conn=sqlite3.connect('/home/rhizomatica/fishline.db')
			c = conn.cursor()
			print query
			c.execute(query)
			advertiser = c.fetchone()
			if advertiser is not None:
				advertiser = advertiser[0]
				conn.commit()
				conn.close()
				self.send(30000,sender,'Please contact the advertiser at'+advertiser)
				self.send(30000,advertiser,'Please contact the buyer at'+sender)
			else:
				self.send(30000,sender,'Please reply again, I did not find that advertiser.')
			return
		else:
			self.send(30000,sender,"Welcome to fishline. Contact 43333 for more information.")
	def send(self, frm, sender, text):
		#send the message on behalf of the applcation
		#figure out if the message is bulk. 
		s = sms.SMS()
		try:
        		s.send(frm, sender, text)
        	#sms.send_broadcasit('antani')
    		except SMSException as e:
    			print "Error: %s" % e

    	def sendbulk(self, sender, text):
		#send the message on behalf of the applcation
		#figure out if the message is bulk. 
		s = sms.SMS()
		try:
        	#s.send(20000, sender, text)
        		s.send_broadcast_from(text,'all',sender)
			#sms.send_broadcast(text,'all')
    		except SMSException as e:
    			print "Error: %s" % e

class summarization:
	def __init__(self):
		self.state = {}

	#def receive(self, sender,text)

	 
if __name__ == '__main__':
	fish = fishline()
	#fish.receive('11221148054',"advertise potato")
	#fish.receive('11221148054',"yes")
	#fish.receive('11221127419','yes TA')
	#fish.getState('1122114')
	#fish.setState('1122114','hello')
	#fish.setState('1122114','hellow2')
	#fish.setAdd('11221148054','advertise new potato');
	#print fish.checkAdvertiser('11221148054');
	fish.receive('11221148054','30000','yes TA');
	#fish.receive('11221148054','20000','yes');
	
	#fish.sendbulk('30000','hello all');
