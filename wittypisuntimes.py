


# suntime has an issue with the day returned for sunset
# https://github.com/SatAgro/suntime/issues/30


from datetime import datetime 
from datetime import timedelta 
from smbus2 import SMBus

from suntime import Sun, SunTimeException
from dateutil import tz
import logging
from logging.handlers import TimedRotatingFileHandler

LATITUDE = -37.840935
LONGITUDE = 144.946457
TIMEZONE = 'Australia/Melbourne'
LOGFILE = '/home/pi/wittypisuntimes.log'

I2C_MC_ADDRESS=0x08

I2C_ID=0
I2C_VOLTAGE_IN_I=1
I2C_VOLTAGE_IN_D=2
I2C_VOLTAGE_OUT_I=3
I2C_VOLTAGE_OUT_D=4
I2C_CURRENT_OUT_I=5
I2C_CURRENT_OUT_D=6
I2C_POWER_MODE=7
I2C_LV_SHUTDOWN=8
I2C_ALARM1_TRIGGERED=9
I2C_ALARM2_TRIGGERED=10
I2C_ACTION_REASON=11
I2C_FW_REVISION=12

I2C_CONF_ADDRESS=16
I2C_CONF_DEFAULT_ON=17
I2C_CONF_PULSE_INTERVAL=18
I2C_CONF_LOW_VOLTAGE=19
I2C_CONF_BLINK_LED=20
I2C_CONF_POWER_CUT_DELAY=21
I2C_CONF_RECOVERY_VOLTAGE=22
I2C_CONF_DUMMY_LOAD=23
I2C_CONF_ADJ_VIN=24
I2C_CONF_ADJ_VOUT=25
I2C_CONF_ADJ_IOUT=26

I2C_CONF_SECOND_ALARM1=27
I2C_CONF_MINUTE_ALARM1=28
I2C_CONF_HOUR_ALARM1=29
I2C_CONF_DAY_ALARM1=30
I2C_CONF_WEEKDAY_ALARM1=31

I2C_CONF_SECOND_ALARM2=32
I2C_CONF_MINUTE_ALARM2=33
I2C_CONF_HOUR_ALARM2=34
I2C_CONF_DAY_ALARM2=35
I2C_CONF_WEEKDAY_ALARM2=36

I2C_CONF_RTC_OFFSET=37
I2C_CONF_RTC_ENABLE_TC=38
I2C_CONF_FLAG_ALARM1=39
I2C_CONF_FLAG_ALARM2=40

I2C_CONF_IGNORE_POWER_MODE=41
I2C_CONF_IGNORE_LV_SHUTDOWN=42

I2C_CONF_BELOW_TEMP_ACTION=43
I2C_CONF_BELOW_TEMP_POINT=44
I2C_CONF_OVER_TEMP_ACTION=45
I2C_CONF_OVER_TEMP_POINT=46
I2C_CONF_DEFAULT_ON_DELAY=47

I2C_LM75B_TEMPERATURE=50
I2C_LM75B_CONF=51
I2C_LM75B_THYST=52
I2C_LM75B_TOS=53

I2C_RTC_CTRL1=54
I2C_RTC_CTRL2=55
I2C_RTC_OFFSET=56
I2C_RTC_RAM_BYTE=57
I2C_RTC_SECONDS=58
I2C_RTC_MINUTES=59
I2C_RTC_HOURS=60
I2C_RTC_DAYS=61
I2C_RTC_WEEKDAYS=62
I2C_RTC_MONTHS=63
I2C_RTC_YEARS=64
I2C_RTC_SECOND_ALARM=65
I2C_RTC_MINUTE_ALARM=66
I2C_RTC_HOUR_ALARM=67
I2C_RTC_DAY_ALARM=68
I2C_RTC_WEEKDAY_ALARM=69
I2C_RTC_TIMER_VALUE=70
I2C_RTC_TIMER_MODE=71

HALT_PIN=4    # halt by GPIO-4 (BCM naming)
SYSUP_PIN=17  # output SYS_UP signal on GPIO-17 (BCM naming)
CHRG_PIN=5    # input to detect charging status
STDBY_PIN=6   # input to detect standby status
    
def bcd2dec( bcd ): 
	dec = (bcd & 0x0F) + (bcd >> 4) * 10
	return dec
	
def dec2bcd(dec): 
	bcd = int( dec / 10 ) * 16 + dec % 10
	return bcd	
    
def get_startup_time(): 
	second = bcd2dec( SMBus(1).read_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_SECOND_ALARM1 ) )
	minute = bcd2dec(SMBus(1).read_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_MINUTE_ALARM1 ) )
	hour = bcd2dec(SMBus(1).read_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_HOUR_ALARM1 ) )
	day = bcd2dec(SMBus(1).read_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_DAY_ALARM1 ) )
	print( "Witty Pi 4 Startup: {0:02d} {1:02d}:{2:02d}:{3:02d}".format(  day , hour , minute , second ) )
	return day , hour , minute , second
	
def set_startup_time( day , hour , minute , second ):
    SMBus(1).write_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_SECOND_ALARM1 , dec2bcd(second) )
    SMBus(1).write_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_MINUTE_ALARM1 , dec2bcd(minute) )
    SMBus(1).write_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_HOUR_ALARM1 , dec2bcd(hour) )
    SMBus(1).write_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_DAY_ALARM1 , dec2bcd(day ) )

    
def get_shutdown_time(): 
	second = bcd2dec( SMBus(1).read_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_SECOND_ALARM2 ) )
	minute = bcd2dec(SMBus(1).read_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_MINUTE_ALARM2 ) )
	hour = bcd2dec(SMBus(1).read_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_HOUR_ALARM2 ) )
	day = bcd2dec(SMBus(1).read_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_DAY_ALARM2 ) )
	print( "Witty Pi 4 Shutdown : {0:02d} {1:02d}:{2:02d}:{3:02d}".format(  day , hour , minute , second ) )
	return day , hour , minute , second
    
def set_shutdown_time( day , hour , minute , second ):
    SMBus(1).write_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_SECOND_ALARM2 , dec2bcd(second) )
    SMBus(1).write_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_MINUTE_ALARM2 , dec2bcd(minute) )
    SMBus(1).write_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_HOUR_ALARM2 , dec2bcd(hour) )
    SMBus(1).write_byte_data(I2C_MC_ADDRESS ,  I2C_CONF_DAY_ALARM2 , dec2bcd(day ) )
    
def sunrise_sunset():
    sun = Sun( LATITUDE, LONGITUDE )
    sunrise = sun.get_sunrise_time( datetime.now() , tz.gettz( TIMEZONE) )
    sunset = sun.get_sunset_time( datetime.now() , tz.gettz( TIMEZONE) )
    return sunrise, sunset
    
#startup_day , startup_hour , startup_minute , startup_second = get_startup_time()
#set_startup_time( startup_day , startup_hour , startup_minute , startup_second  )
#startup_day , startup_hour , startup_minute , startup_second = get_startup_time()

#shutdown_day , shutdown_hour , shutdown_minute , shutdown_second = get_shutdown_time()
#set_shutdown_time( shutdown_day , shutdown_hour , shutdown_minute , shutdown_second  )
#shutdown_day , shutdown_startup_hour , shutdown_minute , shutdown_second = get_shutdown_time()

logging.basicConfig(filename= LOGFILE, format='%(asctime)s %(message)s')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

fileHandler = TimedRotatingFileHandler( LOGFILE, backupCount=2, when="D" , interval=30)

# Get the sunrise and sunset times
sunrise, sunset = sunrise_sunset()
print('Sun Rise at {} Sunset {}'.
      format(sunrise.strftime('%H:%M:%S'), sunset.strftime('%H:%M:%S')))
      
# There is a bug in the date it returns so ignore the day      
today = datetime.now() 
tomorrow = datetime.now() + timedelta(days=1)

# Update Sunset to Witty Pi 4 shutdown
set_shutdown_time(  today.day, sunset.hour  , sunset.minute ,  sunset.second )
logging.info( "Shutdown set: %d %d:%d:%d" , today.day, sunset.hour  , sunset.minute , sunset.second  )


# Update Sunrise to Witty Pi 4 startup
set_startup_time(  tomorrow.day , sunrise.hour  , sunrise.minute , sunrise.second )
logging.info( "Startup set: %d %d:%d:%d" ,  tomorrow.day , sunrise.hour  , sunrise.minute , sunrise.second )


