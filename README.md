# Furbexa

The victim, looking scared...

[[!fear](images/fear.thumbnail.jpg)<br/>(click to enlarge)](images/fear.JPG)

The idea and the majority of the setup came form [a blog post](https://howchoo.com/g/otewzwmwnzb/amazon-echo-furby-using-raspberry-pi-furlexa)
However, there were lots of problems and differences.
Namely

* the code here is different
* the components are squeezed in differently
* gyroscope

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