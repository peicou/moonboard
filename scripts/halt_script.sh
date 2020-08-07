#! /bin/sh

### BEGIN INIT INFO
# Provides:          halt_script.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# to install:
# sudo cp halt_script.sh /etc/init.d/
# sudo chmod +x /etc/init.d/halt_script.sh
# sudo update-rc.d halt_script.sh defaults

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting halt_script.py"
    export PYTHONPATH="/home/pi/.local/lib/python3.7/site-packages"
    /usr/bin/python3 /usr/local/bin/halt_script.py &
    ;;
  stop)
    echo "Stopping halt_script.py"
    pkill -f /usr/local/bin/halt_script.py
    ;;
  *)
    echo "Usage: /etc/init.d/halt_script.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
