import asyncio
from bleak import BleakScanner, BleakClient

HEART_RATE_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HEART_RATE_MEASUREMENT_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

def heart_rate_callback(sender: str, data: bytearray):
    flags = data[0]
    hr_format_bit = flags & 0x01
    if hr_format_bit == 0:
        heart_rate = data[1]
    else:
        heart_rate = int.from_bytes(data[1:3], byteorder='little')
    print(f"Heart Rate: {heart_rate} bpm")

async def connect_and_subscribe():
    print("Scanning for Polar H9/H10 device...")
    devices = await BleakScanner.discover(timeout=10.0)
    target_device = None
    for d in devices:
        if d.name is not None and "Polar" in d.name:
            target_device = d
            print(f"Found device: {d.name} [{d.address}]")
            break
    
    if target_device is None:
        print("No Polar device found. Check if it's awake and in range.")
        return

    # Increase connection timeout and try a direct connect
    async with BleakClient(target_device.address, timeout=20.0) as client:
        if await client.is_connected():
            print("Connected successfully!")
        else:
            print("Could not connect to the Polar device.")
            return

        # Start notifications
        await client.start_notify(HEART_RATE_MEASUREMENT_CHAR_UUID, heart_rate_callback)
        print("Receiving heart rate data. Press Ctrl+C to stop.")

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Stopping notifications...")
            await client.stop_notify(HEART_RATE_MEASUREMENT_CHAR_UUID)

if __name__ == "__main__":
    asyncio.run(connect_and_subscribe())
