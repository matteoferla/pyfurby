# Python API

This is the way to control easily in Python3 a Furby as configured in [hardware](hardware.md) and [software](software.md) pages.

    from pyfurby import Furby
    furby = Furby()
    furby.say('Hello world')
    
If the Furby has any differences from my set-up

* `pwma`: int = 22, motor driver speed - white
* `stby`: int = 4, motor driver on
* `ain1`: int = 27, motor driver forward
* `ain2`: int = 17, motor driver reverse
* `cycle`: int = 21, revolution button (pull-up input)
* `red`: int = 14, red LED (output)
* `green`: int = 24, green LED (output)
* `mouth`: int = 18, mouth button (pull-up input)
* `chest`: int = 20, chest button (pull-up input)
* `back: int` = 16, back button (pull-up input)
* `voice_name`: str = 'en-scottish+m4', espeak/pyttsx3
* `voice_volume`: int = 0.7, espeak/pyttsx3
* `voice_rate`: int = 200, espeak/pyttsx3

It has some preset actions, such as:
    
    furby.ambulance() # make its LED flash like an ambulance
    furby.yell("I am angry")
    furby.shut_eyes(quickly=False)
    furby.fall_asleep() # even slower
    furby.dance() # Ehr? That a seizure.
    furby.flutter() # "blink" salaciously
    furby.blink()
    
 
## Motor

These are all small snippets using the same motor controls:

    furby.set_percent_speed(70) # a value between 55 and 100 percent.
    furby.move_clockwise() # background movement
    furby.move_counterclockwise()
    furby.halt()
    furby.complete_revolution() # eyes wide open
    furby.wait_until_revolution()

The speed is not linear and will depend on how charged the batteries are.
It is quite tricky to time as there revolution completion trigger stays pressed for several degrees worth of rotation
and the motor struggles below 55s and moves in jerks.
The motor is powered by 3.3V, the percentage is already converted from hexadecimal (0xffff is 100%).

| Speed | Rev time |
| ---- | ---- |
| 45% | ~27 s |
| 48% | ~16 s |
| 50% | 7-10 s |
| 52% | 7-9 s |
| 53% | 6.6 s |
| 55% | 5.5 s |
| 60% | 4.5 s |
| 70% | 3.3 s |
| 80% | 2.6 s |
| 90% | 2.2 s |
| 100% | 1.9 s |


## Talk

The gender on espeak/pyttsx3 is controlled by adding `+m1` to `+m4` for male or `+f1` to `+f4` for female after the voice id.
To get the full list of voices:

    for i, voice in enumerate(furby.engine.getProperty('voices')):
        print(f'No. {i} - {voice.name} ({voice.id}) in {voice.languages} of gender {voice.gender} and age {voice.age}')

In English:

* `default`
* `english`
* `en-scottish`
* `english-north`
* `english_rp`
* `english_wmids` (West Midlands)
* `english-us`
* `en-westindies`

## Loop

Given a dictionary with key one of the `furby.permitted_actions` ('lifted', 'moved', 'bitten', 'squeezed', 'aft_squeezed', 'fore_squeezed'),
and value a function, `furby.loop_actions` will call those function when those action is triggered.

Most of these permitted actions have a `wait_until_xxx` method. None of these are asynchronous.

    furby.loop_actions({'lifted': lambda: furby.yell('Put me down now!'),
                        'squeezed': furby.fall_asleep,
                        })




    
