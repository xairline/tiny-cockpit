import time
from utils.XPlaneInstance import XPlaneIpNotFound, XPlaneTimeout, XPlaneUdp
from utils.display import Display
from layers.com1 import COM1
from layers.com2 import COM2


def main():

    display = Display()
    display.show("Search for XP ...", "", "")
    print()
    print("====================================")
    xp = XPlaneUdp()
    while True:
        try:
            beacon = xp.FindIp()
            # single display
            layers = {
                "com1": COM1(xp, display),
                "com2": COM2(xp, display),
                # "nav1": NAV1(display),
                # "nav2": NAV2(display),
                # "adf1": ADF1(display),
                # "adf2": ADF2(display),
            }

            # # double display
            # display2 = Display(address=0x3d)
            # layers = {
            #     "com1": COM1(xp, display),
            #     "com2": COM2(xp, display2),
            #     # "nav1": NAV1(display),
            #     # "nav2": NAV2(display),
            #     # "adf1": ADF1(display),
            #     # "adf2": ADF2(display),
            # }
            lastValuesHash = 0
            active_layer = "com1"
            print("====================================")
            print(f"X Plane IP: {beacon['IP']}")
            print(f"X Plane Port: {beacon['Port']}")
            print(f"X Plane Hostname: {beacon['hostname']}")
            print("====================================")
            print(f"Active layer: {active_layer}")
            print(f"Layers: {layers}")
            print("Starting main loop")
            while True:
                values = xp.GetValues()
                valuesHash = hash(str(values))
                if valuesHash == lastValuesHash:
                    # No new data
                    # skip this iteration as communication is slow to i2c display
                    continue
                else:
                    lastValuesHash = valuesHash
                    # TODO: multiple displays
                    match active_layer:
                        case "com1":
                            layers["com1"].show(values)
                        case "com2":
                            layers["com2"].show(values)
        except Exception as e:
            if isinstance(e, XPlaneTimeout):
                display.error("Error", "XPlane Timeout", "Is Plane loaded?")
            elif isinstance(e, XPlaneIpNotFound):
                display.error("Error", "XPlane not found", "Is XP Running?")
            else:
                print(f"Exception type: {type(e)}")
            time.sleep(1)
            continue


if __name__ == "__main__":
    main()
