# WittyP4-Suntimes
WittyPi 4 Start on Sunrise , Shutdown on Sunset

To use
- remove the default WittyPi schedule /home/pi/wittypu/schedule.wpi
- place wittypisuntimes.py in /home/pi and change the Timezone and Lat/Long
- add this to cron
  @reboot (sleep 20;/usr/bin/python /home/pi/wittypisuntimes.py)&

- and optionally this
  1 0 * * * /usr/bin/python /home/pi/wittypisuntimes.py 
  
