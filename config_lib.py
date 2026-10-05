#!/usr/bin/env python3
"""Load / save user config for AC1 DualSense mapper."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "stick_deadzone": 0.18,
    "trigger_threshold": 0.12,
    "camera_sensitivity": 1.0,
    "buttons": {
        "cross": "A",
        "circle": "B",
        "square": "X",
        "triangle": "Y",
        "l1": "LB",
        "r1": "RB",
        "create": "Back",
        "options": "Start",
        "ps": "Guide",
        "l3": "LS",
        "r3": "RS",
    },
}

# DualSense physical button -> config key
DUALSENSE_KEYS = [
    ("cross", "✕ Cross (крестик)"),
    ("circle", "○ Circle (круг)"),
    ("square", "□ Square (квадрат)"),
    ("triangle", "△ Triangle (треугольник)"),
    ("l1", "L1"),
    ("r1", "R1"),
    ("create", "Create"),
    ("options", "Options"),
    ("ps", "PS"),
    ("l3", "L3 (нажатие левого стика)"),
    ("r3", "R3 (нажатие правого стика)"),
]

# What each Xbox output means in AC1
XBOX_ACTIONS = [
    ("A", "A — Ноги / blend / free-run (с R1)"),
    ("B", "B — Пустая рука / захват"),
    ("X", "X — Атака / оружие"),
    ("Y", "Y — Голова / Eagle Vision"),
    ("LB", "LB — Лок на цель"),
    ("RB", "RB — High Profile"),
    ("Back", "Back — Карта"),
    ("Start", "Start — Пауза"),
    ("Guide", "Guide — кнопка Xbox/PS"),
    ("LS", "LS — нажатие левого стика"),
    ("RS", "RS — центр камеры"),
    ("None", "Выключено"),
]

XBOX_LABEL_TO_CODE = {
    "A": "BTN_A",
    "B": "BTN_B",
    "X": "BTN_X",
    "Y": "BTN_Y",
    "LB": "BTN_TL",
    "RB": "BTN_TR",
    "Back": "BTN_SELECT",
    "Start": "BTN_START",
    "Guide": "BTN_MODE",
    "LS": "BTN_THUMBL",
    "RS": "BTN_THUMBR",
    "None": None,
}

DUALSENSE_TO_EVDEV = {
    "cross": "BTN_SOUTH",
    "circle": "BTN_EAST",
    "square": "BTN_WEST",
    "triangle": "BTN_NORTH",
    "l1": "BTN_TL",
    "r1": "BTN_TR",
    "create": "BTN_SELECT",
    "options": "BTN_START",
    "ps": "BTN_MODE",
    "l3": "BTN_THUMBL",
    "r3": "BTN_THUMBR",
}


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def normalize_config(data: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = deepcopy(DEFAULT_CONFIG)
    if not data:
        return cfg

    cfg["stick_deadzone"] = _clamp(float(data.get("stick_deadzone", cfg["stick_deadzone"])), 0.0, 0.8)
    cfg["trigger_threshold"] = _clamp(
        float(data.get("trigger_threshold", cfg["trigger_threshold"])), 0.0, 0.9
    )
    cfg["camera_sensitivity"] = _clamp(
        float(data.get("camera_sensitivity", cfg["camera_sensitivity"])), 0.2, 2.5
    )

    buttons = dict(cfg["buttons"])
    incoming = data.get("buttons") or {}
    valid = {code for code, _ in XBOX_ACTIONS}
    for key, _label in DUALSENSE_KEYS:
        value = str(incoming.get(key, buttons[key]))
        if value not in valid:
            value = buttons[key]
        buttons[key] = value
    cfg["buttons"] = buttons
    return cfg


def load_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or CONFIG_PATH
    if not config_path.exists():
        save_config(DEFAULT_CONFIG, config_path)
        return deepcopy(DEFAULT_CONFIG)
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return deepcopy(DEFAULT_CONFIG)
    return normalize_config(data)


def save_config(config: dict[str, Any], path: Path | None = None) -> Path:
    config_path = path or CONFIG_PATH
    clean = normalize_config(config)
    config_path.write_text(
        json.dumps(clean, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return config_path
