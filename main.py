import threading
from layers.stat1 import STAT1
from layers.stat2 import STAT2
from utils.XPlaneInstance import XPlaneIpNotFound, XPlaneTimeout, XPlaneUdp
from utils.display import Display
from layers.com1 import COM1
from layers.com2 import COM2


def main():

    display = Display(address=0x3D)
    display2 = Display(address=0x3C)
    display.show("Search for XP ...", "", "")
    display2.show("Search for XP ...", "", "")
    print()
    print("====================================")
    xp = XPlaneUdp()
    # Global variable to store latest values and synchronization lock
    values_lock = threading.Lock()

    def fetch_values(xp):
        global latest_values
        while True:
            try:
                values = xp.GetValues()

                # Acquire lock to update the shared values dictionary
                latest_values = values
            except XPlaneTimeout:
                # Handle XPlaneTimeout if needed
                pass

    def display_layers():
        global latest_values
        lastValuesHash = None

        while True:
            # Acquire lock to read the shared values safely
            values = latest_values.copy()

            valuesHash = hash(str(values))
            if valuesHash == lastValuesHash:
                # No new data
                continue
            else:
                lastValuesHash = valuesHash
                # TODO: multiple displays
                match active_layer:
                    case "com1":
                        layers["com1"].show(values)
                    case "com2":
                        layers["com2"].show(values)
                    case "com":
                        layers["com"][0].show(values)
                        layers["com"][1].show(values)
                    case "stats":
                        layers["stats"][0].show(values)
                        layers["stats"][1].show(values)

            # Let the display thread run at its own pace, adjust the sleep interval as needed
            # time.sleep(0.1)

    while True:
        try:
            beacon = xp.FindIp()
            layers = {
                "com": [COM1(xp, display), COM2(xp, display2)],
                "stats": [STAT1(xp, display), STAT2(xp, display2)],
            }
            active_layer = "stats"
            print("====================================")
            print(f"X Plane IP: {beacon['IP']}")
            print(f"X Plane Port: {beacon['Port']}")
            print(f"X Plane Hostname: {beacon['hostname']}")
            print("====================================")
            print(f"Active layer: {active_layer}")
            print(f"Layers: {layers}")
            print("Starting main loop")
            # Start the value fetching thread
            fetch_thread = threading.Thread(target=fetch_values, args=(xp,))
            fetch_thread.daemon = (
                True  # Daemon thread will exit when the main program exits
            )
            fetch_thread.start()

            # Display layers (runs in the main thread)
            display_layers()
        except KeyboardInterrupt:
            print("\nProcess interrupted by user (Ctrl+C)")
            display.clear()
            display2.clear()
            # Exit the program
            exit(0)
        except Exception as e:
            if isinstance(e, XPlaneTimeout):
                display.error("Error", "XPlane Timeout", "Is Plane loaded?")
                display2.error("Error", "XPlane Timeout", "Is Plane loaded?")
            elif isinstance(e, XPlaneIpNotFound):
                display.error("Error", "XPlane not found", "Is XP Running?")
                display2.error("Error", "XPlane Timeout", "Is Plane loaded?")
            else:
                print(f"Exception type: {type(e)}")
            continue


if __name__ == "__main__":
    main()
