# PyFurby
Control a Raspberry Pi Zero enpowered furby via a served Jupyter notebook or via a restless API.

The victim, looking scared...

[![fear](images/fear.thumbnail.jpg)<br/>(click to enlarge)](images/fear.JPG)

## Module details and functionality

See [API notes](API.md)

The objective is to make the furby easy to control and customise. Say
    
    from pyfurby import Furby
    furby = Furby()
    furby.wait_until_squeezed()
    furby.say('Get your filthy hands off me')
    furby.wait_until_moved()
    furby.say('Put me down you degenerate')
    
It contains several methods, ranging from the comical
    
    furby.flutter() # it flutters its eyelids
    
to the useful 
   
    furby.recite_ip()

## Background

The idea and the majority of the setup came form [a blog post](https://howchoo.com/g/otewzwmwnzb/amazon-echo-furby-using-raspberry-pi-furlexa)
However, there were lots of problems and differences.
Namely

* the code here is different
* the components are squeezed in differently
* gyroscope

## Project
This project can be divided into:

* [hardware](hardware.md)
* [software](software.md)

On the software side, I was disappointed that Alexa not on an Echo cannot play music.
However, making it serve a jupyter notebook and having a nice API (`pyfurby`) mean that it's rather fun.
As a result it is not a Furbexa, but a pyfurby. What do you reckon Furby?

    from pyfurby import Furby
    furby = Furby()
    furby.say('I rather have my fur back on, you creep!')

In fact, I am going to find someone who can sew to make it a lab coat so it can give instructions at open days.