from pycaw.pycaw import AudioUtilities, AudioDeviceState
import warnings
warnings.filterwarnings("ignore")

def get_active_microphones():
    devices = AudioUtilities.GetAllDevices()
    active_decive = []

    for device in devices:
        if device.state == AudioDeviceState.Active:
            active_decive.append(device)

    return active_decive