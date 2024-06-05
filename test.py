import serial, time

ser = serial.Serial("dev/ttyS11", 9600, timeout=5)
probe_fixed_velocity = 6000 # in m/s
carbon_steel_velocity = 5920 # in m/s

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
        th_raw = int(r.decode('utf-8'))
        th_raw *= carbon_steel_velocity / probe_fixed_velocity
        
        # if Hi-Res and Lo-Range
        if res != 0 and rng == 0:
            value = f"{th_raw/100:.2f} mm"
        else:
            value = f"{th_raw/10:.2f} mm"

        print(value)

    time.sleep(0.25)

except KeyboardInterrupt:
    ser.close()