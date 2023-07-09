# Set global variables

lidar_refreshrate = 20 #Hz
# TFmini 2 readout on Raspberry Pi Pico does not work responsively
# with frame rate set to anything higher than 30Hz at 115200 baud rate.

# Generally:
# 1Hz-5Hz usable for non-critical range sensing (slow response application)
# 6Hz-9Hz good frame rate for semi-critical range sensing
# 10Hz-30Hz best for super critical range sensing

# 20 Hz seems to have worked well when measuring speed.
