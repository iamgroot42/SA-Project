import os
import datetime
import requests
import re
import json
import sys

try:
	port=sys.argv[1]
except:
	print "Too few arguments (Provide port)"
	exit()
 
link=raw_input("Enter clone URL (HTTPS/SSH) of deadline-repository\n")
#Extracting name of repo from link :
reponame=link.split('/')[-1].split('.git')[0] 
path=os.path.abspath(os.getcwd())

while True:
	time=raw_input("Enter deadline for submission (DD MM YYYY HH MM)\n")
	time=time.split(' ')
	try:
		timex=datetime.datetime(int(time[2]),int(time[1]),int(time[0]),int(time[3]),int(time[4]))
		assert(timex>datetime.datetime.now())
		break
	except: 
		print "Invalid date"

print("> Deadline  Details :\n")
print("  Deadline name : "+reponame)
print("  Deadline for submission : "+str(timex))
choice=raw_input("> Confirm deadline? (y/n) ")
if(choice=='y' or choice=='Y'):
	#Read from file of users
	try:
		f=open('students','r')
	except:
		print "File of students' list not found"
		exit()
	for line in f:
		line=line.rstrip('\n')
		userid=line.split(' ')[1]
		params={"clone_addr":link,"uid":userid,"repo_name":reponame,"private":"true"}
		r=requests.post("http://localhost:"+port+"/api/v1/repos/migrate", data = params)
		try:
			assert(r.status_code/100==2) #2xx return code <-> Success
		except:
			print "Error initializing data into users' repositories"
			exit()
	f=open(reponame+'_deadline','w')
	f.write(timex.strftime("%Y-%m-%d %H:%M"))
	f.close()
	print("Deadline job created!")
	# Change this to deadline time + 5 minutes :
	automation="at "+time[3]+":"+time[4]+" "+time[1]+"/"+time[0]+"/"+time[2]
	automation+=" << "+"bash prepare.sh"
	os.system(automation)
else:
  print("Deadline not created")	