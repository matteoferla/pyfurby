## Instance attributes

* ain1_pin (DigitalInOut)
* ain2_pin (DigitalInOut)
* back_pin (DigitalInOut)
* chest_pin (DigitalInOut)
* cycle_pin (DigitalInOut)
* engine (Engine)
* green_pin (DigitalInOut)
* gyro (mpu6050)
* mouth_pin (DigitalInOut)
* pwm_pin (PWMOut)
* red_pin (DigitalInOut)
* standby_pin (DigitalInOut)
* use_temporarily (type)

## Class or dynamic attributes

* acceleration (dict)
* aft_squeezed (bool)
* bitten (bool)
* fore_squeezed (bool)
* high_speed (int)
* lifted (bool)
* moved (bool)
* percent_speed (float)
* permitted_actions (list)
* playing (bool)
* rate (int)
* resting_x (float)
* resting_y (float)
* resting_z (float)
* soundcard_status_file (str)
* speed (dict)
* squeezed (bool)
* temperature (float)
* volume (float)

## Methods

#### action_cycle (Furby.action_cycle)
actions=typing.Dict[str, typing.Callable]
This runs a single cycle
Given a dictionary of actions, where the key is an trigger (past particle, e.g. ``bitten``)
and vale is a function to be called if the trigger is true.

:param actions: dictionary of trigger name --> action function to call
:return:

#### ambulance (FurbyCompound.ambulance)
cycles=<class 'int'>

#### background (BackFurby.background)
command=typing.Union[str, typing.Callable]
Run a command in the background.
It is a fake-overloaded function where command is either a str (name of method to be called)
or a method to be called.

>>> furby.background('ambulance', 10)

or

>>> furby.background(furby.ambulance, 10)

:param command: method
:param args:
:param kwargs:
:return:

#### bark (FurbyCompound.bark)


#### blink (FurbyCompound.blink)
cycles=<class 'int'>

#### calculate_translation_matrix (FurbyGyro.calculate_translation_matrix)

One day I will write this.
:return:

#### complete_revolution (FurbyMotor.complete_revolution)
speed=typing.Union[int, NoneType]
Move and wait until the motors complete a revolution/cycle
:param speed:
:return:

#### dance (FurbyCompound.dance)
speed=typing.Union[float, NoneType], cycles=<class 'int'>

#### define_static (FurbyGyro.define_static)

The furby is level and not moving, while earth gravity is still the same.
The board is not z axis pointing to zenith, but at an angle
:return:

#### fall_asleep (FurbyCompound.fall_asleep)


#### flutter (FurbyCompound.flutter)
cycles=<class 'int'>

#### get_percent_speed (FurbyMotor.get_percent_speed)


#### halt (FurbyMotor.halt)

Stop motion.

#### inverse (FurbyMotor.inverse)


#### is_lifted (FurbyGyro.is_lifted)

:return: true when lifted

#### is_moved (FurbyGyro.is_moved)

:return: true when moved

#### loop_actions (Furby.loop_actions)
actions=typing.Dict[str, typing.Callable]
Runs on loop the method ``action_cycle``.
Namely, given a dictionary of actions, where the key is an trigger (past particle, e.g. ``bitten``)
and vale is a function to be called if the trigger is true.

:param actions: dictionary of trigger name --> action function to call
:return:

#### move_clockwise (FurbyMotor.move_clockwise)

Start moving fubry clockwise.

#### move_counterclockwise (FurbyMotor.move_counterclockwise)

Start moving fubry counter-clockwise.

#### move_on_play (Furby.move_on_play)

This is for playing sound -not via say/yell.

Holds forever.

#### recite_ip (FurbyTalk.recite_ip)


#### restful (RestlessFurby.restful)

The furby listens on port 1998, the year the Furby was introduced (Nawww).
Note that it is using Flask's internal app serving method, so is not suitable for use over the internet...
:return:

#### say (Furby.say)
text=<class 'str'>, move=<class 'bool'>
convert the ``text`` to speech and play it.

* To say in a different language change ``voice_name``
* To say in a different volume change ``voice_volume`` (0-1)
* To say in a different rate change ``voice_rate` (200 is default).

:param text: text to say
:param move: move while talking
:return:

#### set_percent_speed (FurbyMotor.set_percent_speed)
speed=<class 'int'>
Will convert to high_speed hex (``0xffff``)
:param speed: speed of motor as %.
:return:

#### shut_eyes (FurbyCompound.shut_eyes)


#### wait_until_bitten (FurbyButtons.wait_until_bitten)

Hold until the furby has its mouth pressed

#### wait_until_moved (FurbyGyro.wait_until_moved)

Idle until moved

#### wait_until_revolution (FurbyMotor.wait_until_revolution)

Idle until the motors complete a revolution/cycle (back trigger)

#### wait_until_squeezed (FurbyButtons.wait_until_squeezed)

Hold until the furby is squeezed

#### yell (Furby.yell)

``say`` but at full volume.
With red led for drama.

:param text:
:return:

## Other

#### use_temporarily (TemporaryValue)

A context manager class to set a temporary value.

    >>> TemporaryValue.furby = furby
    >>> with TemporaryValue('red', True):
    >>>     pass
    
The furby bound ``use_temporarily`` knows furby

    >>> with furby.use_temporarily('red', True):
    >>>     pass


## Note

## Methods

This documentation was manually generated with

    from collections import defaultdict

    def sphinxify_vars(obj):
        attributes = defaultdict(list)
        ivars = set(dir(obj)) - set(dir(obj.__class__))
        for key in sorted(dir(obj)):
            if key[0] == '_':
                continue
            attr = getattr(obj, key)
            att_type = attr.__class__.__name__
            if att_type == 'type':
                attributes['instance'].append({'name': key,
                                             'location': attr.__qualname__,
                                             'docstring':attr.__doc__})
            if att_type in ('builtin_function_or_method', 'method-wrapper', 'method'):
                if not hasattr(attr, '__annotations__'):
                    print(key)
                attributes['method'].append({'name': key,
                                             'location': attr.__qualname__,
                                             'arguments': attr.__annotations__,
                                             'docstring':attr.__doc__})
            elif key in ivars:
                attributes['instance_attribute'].append({'name': key, 'type': att_type})
            else:
                attributes['class_attribute'].append({'name': key, 'type': att_type})
        return attributes
    
    attributes = sphinxify_vars(furby)

    print(f'## Methods')
    for m in attributes['method']:
        print(f'#### {m["name"]} ({m["location"]})')
        print(', '.join([f'{k}={t}' for k, t in m["arguments"].items()]))
        if m['docstring'] is None:
            print()
            continue
        for line in m['docstring'].strip().split('\n'):
            print(line.strip())
        print()