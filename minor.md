## Hello World

On start-up the Furby greets by running `python3 welcome.py;`
    
which constains:

    from pyfurby import Furby
    import time
    
    furby = Furby()
    furby.say("Hello World")
    furby.flutter()
    
    while os.popen('hostname -I').read().strip().split('.')[0] != '192':
        furby.say("Awaiting network connection")
        time.sleep(1)
    
    furby.recite_ip()

    
    
    [Unit]
    Description=Welcome
    After=network-online.target
    Wants=network-online.target
    
    [Service]
    Type=simple
    ExecStart=/usr/bin/python3 /home/pi/welcome.py
    
    [Install]
    WantedBy=multi-user.target