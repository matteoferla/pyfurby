## Hello World

On start-up the Furby greets, setting `sudo nano /etc/rc.local` to call `python3 welcome.py &`
    
The latter contains:
    
    #sudo nano /etc/rc.local

    from pyfurby import Furby
    
    furby = Furby()
    furby.say("Hello World")
    furby.flutter()
    furby.recite_ip()