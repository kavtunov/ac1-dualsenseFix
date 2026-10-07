#!/usr/bin/env python3

from __future__ import annotations

import select
import sys
import time

from evdev import AbsInfo, InputDevice, UInput, ecodes, list_devices

from config_lib import (
    DUALSENSE_TO_EVDEV,
    XBOX_LABEL_TO_CODE,
    load_config,
)

TARGET_NAME = "DualSense Wireless Controller"
POLL_DT = 0.004
AXIS_MAX = 32767
TRIG_MAX = 255


def find_dualsense() -> InputDevice | None:
    for path in list_devices():
        dev = InputDevice(path)
        if dev.name == TARGET_NAME:
            return dev
    return None


def find_all_dualsense_nodes() -> list[InputDevice]:
    nodes: list[InputDevice] = []
    for path in list_devices():
        dev = InputDevice(path)
        if "DualSense Wireless Controller" in dev.name:
            nodes.append(dev)
    return nodes


def build_xbox_pad() -> UInput:
    abs_info_stick = AbsInfo(
        value=0, min=-AXIS_MAX, max=AXIS_MAX, fuzz=16, flat=128, resolution=0
    )
    abs_info_trig = AbsInfo(value=0, min=0, max=TRIG_MAX, fuzz=0, flat=0, resolution=0)
    abs_info_hat = AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)
    cap = {
        ecodes.EV_KEY: [
            ecodes.BTN_A,
            ecodes.BTN_B,
            ecodes.BTN_X,
            ecodes.BTN_Y,
            ecodes.BTN_TL,
            ecodes.BTN_TR,
            ecodes.BTN_SELECT,
            ecodes.BTN_START,
            ecodes.BTN_MODE,
            ecodes.BTN_THUMBL,
            ecodes.BTN_THUMBR,
        ],
        ecodes.EV_ABS: [
            (ecodes.ABS_X, abs_info_stick),
            (ecodes.ABS_Y, abs_info_stick),
            (ecodes.ABS_RX, abs_info_stick),
            (ecodes.ABS_RY, abs_info_stick),
            (ecodes.ABS_Z, abs_info_trig),
            (ecodes.ABS_RZ, abs_info_trig),
            (ecodes.ABS_HAT0X, abs_info_hat),
            (ecodes.ABS_HAT0Y, abs_info_hat),
        ],
    }
    return UInput(
        cap,
        name="Microsoft X-Box 360 pad",
        vendor=0x045E,
        product=0x028E,
        version=0x0110,
        bustype=ecodes.BUS_USB,
    )


def set_btn(ui: UInput, code: int, pressed: bool, state: dict[int, bool]) -> None:
    now = bool(pressed)
    if state.get(code) == now:
        return
    state[code] = now
    ui.write(ecodes.EV_KEY, code, 1 if now else 0)
    ui.syn()


def set_abs(ui: UInput, code: int, value: int, state: dict[int, int]) -> None:
    if state.get(code) == value:
        return
    state[code] = value
    ui.write(ecodes.EV_ABS, code, value)
    ui.syn()


def make_stick_normalizer(deadzone: float, sensitivity: float = 1.0):
    def norm_stick(value: int, info: AbsInfo) -> int:
        mid = (info.min + info.max) / 2.0
        half = max((info.max - info.min) / 2.0, 1.0)
        v = (value - mid) / half
        if abs(v) < deadzone:
            return 0
        sign = 1.0 if v > 0 else -1.0
        mag = (abs(v) - deadzone) / (1.0 - deadzone)
        mag = min(1.0, mag * sensitivity)
        return int(max(-AXIS_MAX, min(AXIS_MAX, sign * mag * AXIS_MAX)))

    return norm_stick


def make_trigger_normalizer(threshold: float):
    def norm_trigger(value: int, info: AbsInfo) -> int:
        span = max(info.max - info.min, 1)
        t = (value - info.min) / span
        if t < threshold:
            return 0
        t = (t - threshold) / (1.0 - threshold)
        return int(max(0, min(TRIG_MAX, t * TRIG_MAX)))

    return norm_trigger


def build_btn_map(buttons: dict[str, str]) -> dict[int, int]:
    mapping: dict[int, int] = {}
    for dual_key, xbox_label in buttons.items():
        dual_name = DUALSENSE_TO_EVDEV.get(dual_key)
        xbox_name = XBOX_LABEL_TO_CODE.get(xbox_label)
        if not dual_name or not xbox_name:
            continue
        dual_code = getattr(ecodes, dual_name)
        xbox_code = getattr(ecodes, xbox_name)
        mapping[dual_code] = xbox_code
    return mapping


def main() -> int:
    cfg = load_config()
    stick_deadzone = float(cfg["stick_deadzone"])
    trigger_threshold = float(cfg["trigger_threshold"])
    camera_sensitivity = float(cfg["camera_sensitivity"])
    norm_stick = make_stick_normalizer(stick_deadzone, 1.0)
    norm_camera = make_stick_normalizer(stick_deadzone, camera_sensitivity)
    norm_trigger = make_trigger_normalizer(trigger_threshold)
    btn_map = build_btn_map(cfg["buttons"])

    print("Waiting for DualSense...")
    pad = None
    while pad is None:
        pad = find_dualsense()
        if pad is None:
            time.sleep(0.4)

    nodes = find_all_dualsense_nodes()
    for node in nodes:
        try:
            node.grab()
        except OSError as exc:
            print(f"grab failed {node.path}: {exc}")

    abs_caps: dict[int, AbsInfo] = {}
    for item in pad.capabilities(absinfo=True).get(ecodes.EV_ABS, []):
        if isinstance(item, tuple):
            code, info = item[0], item[1]
            abs_caps[int(code)] = (
                info if isinstance(info, AbsInfo) else pad.absinfo(int(code))
            )
        else:
            abs_caps[int(item)] = pad.absinfo(int(item))

    axis_names = {code: ecodes.ABS[code] for code in abs_caps}

    def axis_by(*names: str) -> int | None:
        for code, name in axis_names.items():
            if name in names:
                return code
        return None

    def rest_value(code: int) -> int:
        return int(pad.absinfo(code).value)

    def is_centered(code: int | None) -> bool:
        if code is None:
            return False
        info = abs_caps[code]
        mid = (info.min + info.max) / 2.0
        return abs(rest_value(code) - mid) <= (info.max - info.min) * 0.20

    def is_trigger_rest(code: int | None) -> bool:
        if code is None:
            return False
        info = abs_caps[code]
        span = max(info.max - info.min, 1)
        return (rest_value(code) - info.min) / span <= 0.12

    lx, ly = axis_by("ABS_X"), axis_by("ABS_Y")
    rx = ry = None
    for a, b in (
        (axis_by("ABS_RX"), axis_by("ABS_RY")),
        (axis_by("ABS_Z"), axis_by("ABS_RZ")),
    ):
        if is_centered(a) and is_centered(b):
            rx, ry = a, b
            break
    if rx is None:
        rx, ry = axis_by("ABS_RX"), axis_by("ABS_RY")

    triggers = sorted(
        {
            c
            for c in (
                axis_by("ABS_Z"),
                axis_by("ABS_RZ"),
                axis_by("ABS_RX"),
                axis_by("ABS_RY"),
            )
            if c is not None and c not in (lx, ly, rx, ry) and is_trigger_rest(c)
        }
    )
    lt = triggers[0] if len(triggers) > 0 else None
    rt = triggers[1] if len(triggers) > 1 else None

    ui = build_xbox_pad()
    btn_state: dict[int, bool] = {}
    abs_state: dict[int, int] = {}
    axis_values = {code: int(pad.absinfo(code).value) for code in abs_caps}

    print("ready")

    try:
        while True:
            readable, _, _ = select.select([n.fd for n in nodes], [], [], POLL_DT)
            if readable:
                for node in nodes:
                    if node.fd not in readable:
                        continue
                    for event in node.read():
                        if node.path != pad.path:
                            continue
                        if event.type == ecodes.EV_KEY and event.value != 2:
                            mapped = btn_map.get(event.code)
                            if mapped is not None:
                                set_btn(ui, mapped, event.value != 0, btn_state)
                        elif event.type == ecodes.EV_ABS:
                            axis_values[event.code] = event.value
                            if event.code == ecodes.ABS_HAT0X:
                                set_abs(ui, ecodes.ABS_HAT0X, int(event.value), abs_state)
                            elif event.code == ecodes.ABS_HAT0Y:
                                set_abs(ui, ecodes.ABS_HAT0Y, int(event.value), abs_state)

            if lx is not None and ly is not None:
                set_abs(ui, ecodes.ABS_X, norm_stick(axis_values[lx], abs_caps[lx]), abs_state)
                set_abs(ui, ecodes.ABS_Y, norm_stick(axis_values[ly], abs_caps[ly]), abs_state)
            if rx is not None and ry is not None:
                set_abs(
                    ui, ecodes.ABS_RX, norm_camera(axis_values[rx], abs_caps[rx]), abs_state
                )
                set_abs(
                    ui, ecodes.ABS_RY, norm_camera(axis_values[ry], abs_caps[ry]), abs_state
                )
            if lt is not None:
                set_abs(ui, ecodes.ABS_Z, norm_trigger(axis_values[lt], abs_caps[lt]), abs_state)
            if rt is not None:
                set_abs(ui, ecodes.ABS_RZ, norm_trigger(axis_values[rt], abs_caps[rt]), abs_state)
    except KeyboardInterrupt:
        print("stopped")
    finally:
        for node in nodes:
            try:
                node.ungrab()
            except OSError:
                pass
        ui.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
