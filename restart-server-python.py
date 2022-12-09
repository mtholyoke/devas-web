import os

def restart(toKill):
    #if toKill is not empty, kill toKill
    if toKill:
        os.system("kill %d" % toKill)

    #then we run the server
    os.system("./start-dev-server.sh") 

#the first thing that we should do is use ps auwx | grep devas-web
#in order to check if the server is running 
PID = os.system("ps auwx | grep devas-web")
PIDlines = PID.split("\n") #split along entries

toKill = "" #empty if 
#go through lines of PIDlines and find if any contain "superman_server.py"
#if they do, split that line by the word and locate the 'word' at the first index
# i.e, toKill 
for entry in PIDlines:
    if "superman_server.py" in entry:
        splitEntry = entry.split(" ")
        toKill = splitEntry[1]

#kill toKill if possible and use start-dev-server.sh
restart(toKill) 

# check the errors logs to see if the server is actually running
osError = os.system("cat logs/errors.out | grep Address already in use")

if not osError: #i.e, osError is empty
    print("Server has started up! Please remember that some datasets may take a few moments to load.")
    exit()

#if osError is NOT empty, there is another problem
#here we would try the netstat -plnt method of restarting the server

PID = os.system("netstat -plnt")
PIDlines = PID.split("-") #split along hyphens

for entry in PIDlines:
    if "/python3" in entry: #in case port changes
        entry.strip() #remove trailing whitespace
        end = entry.index("/") #find index of hyphen to mark end of PID
        #search for a digit in the likely range of a PID
        start = entry.index(str(x for x in range(0,9)), end-8, end)
        toKill = entry[start:end]

restart(toKill)
print("Server should now have started up!")