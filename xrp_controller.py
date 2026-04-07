import sys
import time
import serial
import tty
import termios
import select

BAUD_RATE = 115200
PORT = '/dev/cu.usbmodem14201'

def main():
    print("Connecting to XRP...")
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
    except serial.SerialException as e:
        print("Could not open port: " + str(e))
        sys.exit(1)

    time.sleep(1.5)
    print("")
    print("==========================================")
    print("  XRP Controller - ready!")
    print("==========================================")
    print("  W   Forward       S   Backward")
    print("  A   Turn Left     D   Turn Right")
    print("  Q   Arc Left      E   Arc Right")
    print("  SPACE / X   Stop")
    print("  +/-  Speed Up/Down")
    print("  ESC or Ctrl-C  Quit")
    print("==========================================")
    print("  Press a key to start moving.")
    print("  Press SPACE or X to stop.")
    print("")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    current_cmd = b' '
    ser.write(current_cmd)

    try:
        tty.setraw(fd)

        while True:
            ready = select.select([sys.stdin], [], [], 0.1)[0]

            if ready:
                ch = sys.stdin.read(1)

                # Quit
                if ch in ('\x1b', '\x03'):
                    break

                # Drain arrow key escape sequences
                if ch == '\x1b':
                    select.select([sys.stdin], [], [], 0.05)
                    continue

                ch = ch.lower()

                if ch == 'w':
                    current_cmd = b'w'
                    sys.stdout.write('\r  Moving: FORWARD     ')
                elif ch == 's':
                    current_cmd = b's'
                    sys.stdout.write('\r  Moving: BACKWARD    ')
                elif ch == 'a':
                    current_cmd = b'a'
                    sys.stdout.write('\r  Moving: TURN LEFT   ')
                elif ch == 'd':
                    current_cmd = b'd'
                    sys.stdout.write('\r  Moving: TURN RIGHT  ')
                elif ch == 'q':
                    current_cmd = b'q'
                    sys.stdout.write('\r  Moving: ARC LEFT    ')
                elif ch == 'e':
                    current_cmd = b'e'
                    sys.stdout.write('\r  Moving: ARC RIGHT   ')
                elif ch in (' ', 'x'):
                    current_cmd = b' '
                    sys.stdout.write('\r  Moving: STOPPED     ')
                elif ch in ('+', '='):
                    current_cmd = b'+'
                    sys.stdout.write('\r  Moving: SPEED UP    ')
                elif ch in ('-', '_'):
                    current_cmd = b'-'
                    sys.stdout.write('\r  Moving: SPEED DOWN  ')

                sys.stdout.flush()

            # Keep sending current command continuously
            ser.write(current_cmd)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        ser.write(b' ')
        time.sleep(0.1)
        ser.close()
        print("\nDisconnected.")

if __name__ == "__main__":
    main()
