import ioled_lib, time

strip = ioled.LedStrip("{IP_ADDRESS}", 2712)

strip.sendRainbow(500, 0.3)

time.sleep(2)

strip.color(255, 0, 0).brightness(0.4).addRange(0, 4).color(0, 255, 0).addRange(4, 8).color(0, 0, 255).addRange(8, 12).send()
time.sleep(2)

strip.color(255, 0, 0).addRange(0, 12).send()
time.sleep(2)

strip.color(0, 255, 0).addRange(0, 12).send()
time.sleep(2)

strip.color(0, 0, 255).addRange(0, 12).send()
time.sleep(2)

bns = []
for i in range(0, 20):
    bns.append(i*0.05)

for x in range(0, 2):
    for i in range(0, len(bns)):
        strip.color(255, 0, 0).brightness(bns[i]).addRange(0, 12).send()
        time.sleep(0.1)
    for i in range(0, len(bns)):
        strip.color(255, 0, 0).brightness(bns[len(bns)-1-i]).addRange(0, 12).send()
        time.sleep(0.1)

for i in range(0, 12):
    strip.color(255, 0, 0).brightness(0.5).addLed(i).send()
    time.sleep(0.1)

for i in range(0, 12):
    strip.color(0, 255, 0).addLed(i).send()
    time.sleep(0.1)

for i in range(0, 12):
    strip.color(0, 0, 255).addLed(i).send()
    time.sleep(0.1)

strip.color(0, 0, 0).addRange(0, 12).send()

for j in range(0, 20):
    for i in range(0, 12):
        strip.color(0, 0, 255).addLed(i).send()
        time.sleep(0.05)

        strip.color(0, 0, 0).addLed(i).send()
