#!/usr/bin/python
# Author : Phinfinity
# email : Anish Shankar <rndanish@gmail.com>
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
#  Usage : ./processtrack.py time_limit(in s) Memory_Limit(in MB) command args..
#  Not memory includes memory required for shared libraries. as a safety marigin
#  13MB is added to the memory limit specified for some basic libraries.
#  Returns 0 on success and prints details
#  Returns 1 on failure
#  The last 5 lines of the output (including the new line at begining of the 5 lines)
#  is part of the status message (TLE/WA/AC, mem used time spent etc.)
#  everything above that is programs output
#  ./processtrack.py 10 32 ./a.out < in | head -n -5 | head -c -1
#  this extracts the exact output (to the byte-whitespace) of ./a.out < in
#

 
import sys,os,resource,time,signal
safety_limit = 13
timelimit = 1.0
memorylimit = 20
memorylimit  = 1024*1024*(memorylimit+safety_limit) #Safety limit
tledelta = 0.2 # No of seconds of execution within which to conclude TLE

def runchild():
    resource.setrlimit(resource.RLIMIT_CPU,(timelimit,timelimit)) 
    resource.setrlimit(resource.RLIMIT_AS,(memorylimit,memorylimit))
    # Also consider RLIMIT_DATA vs RLIMIT_AS ?
    # Conclusion RLIMIT_DATA is better, AS includes linked library inclusions
    # More severe issues later conclusion: RLIMIT_DATA is ignored use RLIMIT_AS
    #resource.setrlimit(resource.RLIMIT_NPROC,(512,512)) # max 1 process
    try:
        os.execvp(sys.argv[3], sys.argv[3:])
    except Exception:
        pass
    sys.exit(2)

cpid = 0
tle = False
def getstatus(retstatus,rusage):
   global tle
   if tle:
       return "TLE"
   else:
       if os.WIFSIGNALED(retstatus):
           if timelimit - rusage.ru_utime < tledelta:
               return "TLE"
           sigdict = {}
           for key in signal.__dict__.keys():
               if key.startswith("SIG"):
                   sigdict[getattr(signal,key)] = key
           return "RunTimeError (%s)" % sigdict[os.WTERMSIG(retstatus)]
       elif os.WIFEXITED(retstatus):
           exitcode = os.WEXITSTATUS(retstatus)
           if exitcode != 0:
               return "NZEC (%d)"%exitcode
   return "Run OK"
def handler(signum, frame):
    global tle
    if signum == signal.SIGALRM:
        print "Killing due to excess realtime",cpid
        tle = True
        os.kill(cpid, signal.SIGKILL)
    elif signum == signal.SIGCHLD:
        (pid, retstatus, rusage) = os.wait3(os.WNOHANG|os.WUNTRACED)
        if (pid != cpid):
            sys.stderr.write("Error invalid child provess exited")
            return
        '''
        print "WCOREDUMP:",os.WCOREDUMP(retstatus)
        print "WIFEXITED:",os.WIFEXITED(retstatus)
        print "WEXITSTATUS:",os.WEXITSTATUS(retstatus)
        print "WIFCONTINUED:",os.WIFCONTINUED(retstatus)
        print "WIFSIGNALED:",os.WIFSIGNALED(retstatus)
        print "WIFSTOPPED:",os.WIFSTOPPED(retstatus)
        print "WSTOPSIG:",os.WSTOPSIG(retstatus)
        print "WTERMSIG:",os.WTERMSIG(retstatus)
        '''

        status =  getstatus(retstatus,rusage)
        print  # This new line is important! important to cut up the last 5 lines of status output
        print status
        print "Program PID",pid
        print "User Time:",rusage.ru_utime
        print "System Time:",rusage.ru_stime
        print "Maximum Resident Set Size (Memory):",rusage.ru_maxrss/1000.0,"MB"
        #print rusage
        if(status == "Run OK"):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print "UNKOWN SIGNAL"

def main():
    if len(sys.argv) <= 3:
        sys.stderr.write("Error. Usage : %s time_limit(in s) Memory_Limit(in MB) command args..\n"%sys.argv[0])
        sys.exit(2)
    global timelimit,memorylimit
    timelimit = float(sys.argv[1])
    memorylimit = 1024*1024*(safety_limit + int(sys.argv[2]))

    global cpid
    cpid = os.fork()
    if cpid == 0:
        runchild()

    signal.signal(signal.SIGALRM, handler)
    signal.signal(signal.SIGCHLD, handler)
    signal.alarm(int(max(1,timelimit*1.5+1)))
    # Set an extra 50% for realtime, CPU time is still fixed
    while(True): time.sleep(10)
    # Sleep in an infinite loop as sleep is interrupted on signal
    # Rest of code execution in signal handler sleep long enough for alarm to ring handler before
    print "Took Too Long Exiting Main"
if __name__=="__main__":
    main()
