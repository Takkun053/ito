import sys

import pystray


def main(icon: pystray._base.Icon):
    icon.visible = True
    print(sys.argv)
