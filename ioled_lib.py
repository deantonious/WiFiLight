import socket

class LedStrip:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.message = "l"

    def color(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        return self

    def brightness(self, br):
        self.br = br
        return self

    def addLed(self, led_n):
        self.message += "{}-{}:{},{},{};".format(led_n, led_n+1, self.r*self.br, self.g*self.br, self.b*self.br)
        return self

    def addRange(self, led_s, led_f):
        self.message += "{}-{}:{},{},{};".format(led_s, led_f, self.r*self.br, self.g*self.br, self.b*self.br)
        return self

    def send(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes(self.message, "utf-8"), (self.ip, self.port))
        self.message = "l"

    def sendRainbow(self, packets, br):
        self.brightness(br)
        for i in range(0, packets):
            (r, g, b) = self.hsv_to_rgb(float(i) / packets, 1.0, 1.0)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            self.color(R, G, B).addRange(0, 12).send()

    # from colorsys
    def hsv_to_rgb(self, h, s, v):
        if s == 0.0:
            return v, v, v
        i = int(h*6.0)
        f = (h*6.0) - i
        p = v*(1.0 - s)
        q = v*(1.0 - s*f)
        t = v*(1.0 - s*(1.0-f))
        i = i%6
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q
