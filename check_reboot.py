#!/usr/local/bin/python2.7

#Homegrown Modules
import logger
import mailer
#Python Modules
import socket
import subprocess

#Variables
hostname = socket.gethostname()
recipeint = "mark@transcendedlife.local"
sender = "%s@transcendedlife.local" % hostname
log = "/var/log/check_reboot.log"

if __name__ == "__main__":
  logger.logMessage(log, "Checking for required reboot.")
  latest_kernel = (subprocess.check_output("rpm -q --last kernel | perl -pe 's/^kernel-(\S+).*/$1/' | head -1", shell=True)).strip()
  active_kernel = (subprocess.check_output("uname -r", shell=True)).strip()
  logger.logMessage(log, "Active Kernel: %s" % active_kernel)
  logger.logMessage(log, "Latest Kernel: %s" % latest_kernel)

  if (active_kernel != latest_kernel):
    logger.logMessage(log, "Required reboot detected. Sending mail.")
    mailer.sendMail(recipeint, sender, "%s requires reboot." % hostname,
                    """Newer Kernel version installed than is actively running.
Reboot %s to resolve.""" % hostname)
  else:
    logger.logMessage(log, "No reboot required.")
  logger.logMessages(log, "===================")
