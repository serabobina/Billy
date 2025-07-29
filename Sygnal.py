import signal
import sys
import constants


def signal_handler(sig, frame):
    print(constants.CTRL_C_message)
    sys.exit(0)


def process_signal():
    signal.signal(signal.SIGINT, signal_handler)
