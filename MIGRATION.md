# Furby on Raspberry Pi OS 13

Migrated on 21 November 2026 from the original Buster card. The original application and configuration archive is in the Mac local-network project's `backups/furby-migration-20261121/` directory. That backup is private: it includes historical service configuration.

The new Zero W uses user `matteo`, application `/home/matteo/apps/pyfurby`, and virtual environment `/home/matteo/furby-venv`. The five recovered notebooks are in `/home/matteo/notebooks`.

## Starting software

Activate the environment with `source ~/furby-venv/bin/activate` before using Python. Importing `pyfurby` does not start the greeting. Constructing `Furby()` configures its GPIO pins and speech engine.

The `greet.service` unit is installed but disabled during wiring work. The greeting defaults to speech only; motor movement requires explicitly supplying `--move`. When wiring and power have been checked, a manual greeting is:

```sh
~/furby-venv/bin/python ~/apps/pyfurby/welcome.py
```

Jupyter is provided by `furby-jupyter.service`, listening on localhost port 8888 with authentication enabled. Connect from the Mac using:

```sh
ssh -L 8888:127.0.0.1:8888 matteo@furby.local
```

Then open `http://127.0.0.1:8888` and use the token stored privately in `~/.config/furby/jupyter-token` on the Pi. The notebooks use the Furby virtual environment kernel. Old notebook outputs are preserved as historical data; old cells may move the motor when explicitly executed.

## Wiring assignments

BCM numbers below match the application defaults. Physical numbers are the standard top-view 40-pin header numbering; this project's board has inverted headers, so use the board orientation carefully. Power down before changing wiring.

| Function | BCM GPIO | Physical pin |
| --- | --- | --- |
| MPU6050 SDA | 2 | 3 |
| MPU6050 SCL | 3 | 5 |
| Motor standby | 4 | 7 |
| Motor direction AIN1 | 27 | 13 |
| Motor direction AIN2 | 17 | 11 |
| Motor speed PWM | 22 | 15 |
| Cycle switch | 12 | 32 |
| Red LED | 14 | 8 |
| Green LED | 24 | 18 |
| Mouth button | 15 | 10 |
| Chest button | 16 | 36 |
| Back button | 26 | 37 |
| I2S bit clock, amp and mic | 18 | 12 |
| I2S word select, amp and mic | 19 | 35 |
| I2S input, microphone DOUT | 20 | 38 |
| I2S output, amplifier DIN | 21 | 40 |

GPIO25 has no header or wire. The custom audio driver reserves it as an unused SDMODE control, with switching disabled; this prevents the standard voiceHAT driver from taking the chest-button GPIO16. GPIO8, GPIO9 and GPIO11 remain unused. Gyro power must use the sensor board's supported supply and share ground; sensor signals are 3.3 V logic. Preserve the existing motor driver power arrangement; the table specifies control signals, not motor supply wiring.

## Audio and diagnostics

The `furby-audio` overlay is adapted from Raspberry Pi Linux's `googlevoicehat-soundcard` overlay for the SPH0645 microphone and MAX98357A output. It requires no obsolete external kernel modules. Do not also load `hifiberry-dac`: these would compete for the same I2S controller.

`aplay -l` and `arecord -l` should both list `sndrpigooglevoi`. ALSA uses that stable card name rather than a changing numeric index. Audio samples must be validated after reconnecting the amp/microphone; device detection alone does not prove physical sound or capture.

```sh
systemctl status furby-jupyter.service greet.service
journalctl -b -u greet.service
journalctl -b -u NetworkManager
```

The old root Jupyter/Slack retry wrapper and legacy AlexaPi service are preserved in the backup and are not autostarted on the new card. Jupyter replaces the old notebook service without restoring obsolete cloud credentials.

## Migration verification

Hardware-free motor regression tests are in `tests/test_motor_safety.py`. The non-actuating `deploy/check-furby.py` script checks imports and registered interfaces. Software PWM uses the current `Adafruit-Blinka-Raspberry-Pi-PWM` backend. Pin objects use `board.D*` rather than the removed public `digitalio.Pin` constructor.

Native GPIO, I2C, PyAudio, NumPy and pandas modules are provided by Trixie packages. Only those modules are linked into the virtual environment; unrelated desktop Python packages are excluded. Some ARM packages retain an embedded armv7 wheel tag despite being distributed for armv6, so `pip check` reports platform-tag warnings. Actual imports and notebook execution must be verified on this Zero W rather than interpreting those warnings as missing dependencies.

## Verified migration result, 21 November 2026

After rebooting the original Zero W Rev 1.1, Wi-Fi rejoined, `/dev/i2c-1` was present, and the custom sound card registered both playback and capture. A one-second 48 kHz capture and synthesized-WAV playback completed at the driver level. All GPIO wires were disconnected: these checks do not verify the physical amplifier, speaker, microphone, gyro or motor.

`Furby()` initialized successfully with standby and direction outputs LOW and PWM duty zero, then all GPIO resources were released. The absent gyro produced a warning and did not abort initialization. All three motor safety regression tests passed. A real notebook kernel executed Furby, pandas, audio and speech-recognition imports. Authenticated Jupyter returned HTTP 200 both before and after reboot. No failed systemd services were present.

Boot now uses `multi-user.target` to conserve resources on the single-core Zero. Desktop packages remain installed; `sudo systemctl set-default graphical.target` restores graphical boot if wanted. The previous target is recorded in `/var/backups/furby/previous-default-target.txt`. Greeting autostart remains disabled. The old card is safely unmounted on the Pi400.

Native scientific/audio packages come from Trixie. `link-system-libraries.py` records the explicit native module links used by this deployment. The ALSA and overlay sources are included alongside them.
