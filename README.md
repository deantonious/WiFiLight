# InternetOfLEDs
Library and Arduino firmware to control Arduino powered RGB lights! 

## Usage
First import it with `import ioled_lib`. Then use `ioled_lib.LedStrip(IP, PORT)` to create the connection with the controller module.

`color(r, g, b)`: set the RGB color used until it's changed by another color call.

`brightness(br)`: set the Brightness (0.00-1.00) used until it's changed by another brightness call.

`addLed(led_n)`: add the LED (position in strip) with the previously set color/brightness.

`addRange(led_s, led_f)`: add a range of LED (initial and end position in strip) with the previously set color/brightness.

The `send()`: send the packet to the controller board.
    
Usage example:
```python
import ioled_lib

strip = ioled_lib.LedStrip("192.168.1.111", 2712)
strip.color(255, 0, 0).addRange(0, 12).send()
```
