import serial, time

ser = serial.Serial("dev/ttyS11", 9600, timeout=5)

try:
    data = ser.read_until(b"\x17")
    print(data)
    status = data[1]
    print(f"Valid reading: {bin(ord(status & 0x01))}")
    print(f"Status: {bin(ord(status))}")

    if len(data) == 3:
        # No valid reading
        pass

    elif len(data) == 7:
        # Valid reading
        res = status & 0b01000000
        rng = status & 0b00010000

        r = data[2:7]
        r = [i.decode("utf-8") for i in r]
        
        # if Hi-Res and Lo-Range
        if res != 0 and rng == 0:
            value = f"{r[0]}{r[1]}.{r[2]}{r[3]} mm"
        else:
            value = f"{r[0]}{r[1]}{r[2]}.{r[3]} mm"

        print(value)

    time.sleep(0.25)

except KeyboardInterrupt:
    ser.close()