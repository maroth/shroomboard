from enum import Enum


class Status(Enum):
    OPTIMAL = 1
    SUBOPTIMAL = 2
    CRITICAL = 3
    CATASTROPHIC = 4


def get_humidity_status(humidity):
    if humidity < 50:
        return Status.CATASTROPHIC, f"Red Alert: Mycelium humidity levels at {humidity} percent! " \
                                    f"Conditions critical! Catastrophic mycelium extinction event is imminent! " \
                                    f"Enact emergency H2O procedures immediately!"
    elif humidity < 70:
        return Status.CRITICAL, f"Yellow alert: Mycelium humidity levels at {humidity} percent! " \
                                f"Critical environmental conditions. Increase humidity immediately."

    elif humidity < 90:
        return Status.SUBOPTIMAL, f"Warning: Mycelium humidity levels at {humidity} percent! " \
                                  f"Suboptimal growth environment. Additional humidity recommended."

    elif humidity < 95:
        return Status.OPTIMAL, f"Optimal mycelium humidity levels at {humidity} percent! " \
                               f"Automated nutrient farm operating within established parameters."

    elif humidity:
        return Status.SUBOPTIMAL, f"Warning: Mycelium humidity levels at {humidity} percent! " \
                                  f"Moisture levels above assigned parameters. Temporary colony chamber evacuation " \
                                  f"recommended."
