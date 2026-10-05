#!/usr/bin/env python3
"""Simple GUI to change DualSense -> Xbox layout for AC1."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from config_lib import (
    CONFIG_PATH,
    DEFAULT_CONFIG,
    DUALSENSE_KEYS,
    XBOX_ACTIONS,
    load_config,
    save_config,
)


class SettingsApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("AC1 DualSense — настройка кнопок")
        self.minsize(520, 640)
        self.geometry("560x700")

        self.config_data = load_config()
        self.button_vars: dict[str, tk.StringVar] = {}
        self.label_to_code = {label: code for code, label in XBOX_ACTIONS}
        self.code_to_label = {code: label for code, label in XBOX_ACTIONS}
        self.deadzone_var = tk.DoubleVar(value=self.config_data["stick_deadzone"])
        self.trigger_var = tk.DoubleVar(value=self.config_data["trigger_threshold"])
        self.camera_var = tk.DoubleVar(value=self.config_data["camera_sensitivity"])

        self._build()

    def _build(self) -> None:
        header = ttk.Label(
            self,
            text="Выбери, что делает каждая кнопка DualSense в игре",
            font=("Sans", 12, "bold"),
            wraplength=500,
            justify="center",
        )
        header.pack(padx=16, pady=(16, 8))

        hint = ttk.Label(
            self,
            text=f"Настройки сохраняются в:\n{CONFIG_PATH}",
            wraplength=500,
            justify="center",
        )
        hint.pack(padx=16, pady=(0, 12))

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=16)

        xbox_labels = [label for _code, label in XBOX_ACTIONS]

        for row, (key, dual_label) in enumerate(DUALSENSE_KEYS):
            ttk.Label(frame, text=dual_label).grid(row=row, column=0, sticky="w", pady=4)
            current = self.config_data["buttons"].get(key, "None")
            var = tk.StringVar(value=self.code_to_label.get(current, self.code_to_label["None"]))
            self.button_vars[key] = var
            combo = ttk.Combobox(
                frame,
                textvariable=var,
                values=xbox_labels,
                state="readonly",
                width=42,
            )
            combo.grid(row=row, column=1, sticky="ew", pady=4, padx=(12, 0))

        frame.columnconfigure(1, weight=1)

        sens = ttk.LabelFrame(self, text="Чувствительность")
        sens.pack(fill="x", padx=16, pady=12)

        self._add_scale(sens, "Мёртвая зона стиков", self.deadzone_var, 0.0, 0.6, 0)
        self._add_scale(sens, "Порог триггеров", self.trigger_var, 0.0, 0.7, 1)
        self._add_scale(sens, "Чувствительность камеры", self.camera_var, 0.2, 2.5, 2)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=16, pady=(0, 16))

        ttk.Button(buttons, text="Сбросить по умолчанию", command=self.reset_defaults).pack(
            side="left"
        )
        ttk.Button(buttons, text="Сохранить", command=self.save).pack(side="right")

        tip = ttk.Label(
            self,
            text="После сохранения перезапусти маппер (./ac1-gamepad.sh),\nчтобы новые кнопки применились.",
            justify="center",
        )
        tip.pack(padx=16, pady=(0, 16))

    def _add_scale(
        self,
        parent: ttk.LabelFrame,
        title: str,
        variable: tk.DoubleVar,
        low: float,
        high: float,
        row: int,
    ) -> None:
        ttk.Label(parent, text=title).grid(row=row, column=0, sticky="w", padx=8, pady=6)
        value_label = ttk.Label(parent, text=f"{variable.get():.2f}")
        value_label.grid(row=row, column=2, sticky="e", padx=8)

        def on_change(_event: object | None = None) -> None:
            value_label.configure(text=f"{variable.get():.2f}")

        scale = ttk.Scale(
            parent,
            from_=low,
            to=high,
            variable=variable,
            command=lambda _v: on_change(),
        )
        scale.grid(row=row, column=1, sticky="ew", padx=8, pady=6)
        parent.columnconfigure(1, weight=1)

    def _collect(self) -> dict:
        buttons = {}
        for key, var in self.button_vars.items():
            buttons[key] = self.label_to_code[var.get()]
        return {
            "stick_deadzone": float(self.deadzone_var.get()),
            "trigger_threshold": float(self.trigger_var.get()),
            "camera_sensitivity": float(self.camera_var.get()),
            "buttons": buttons,
        }

    def save(self) -> None:
        path = save_config(self._collect())
        messagebox.showinfo(
            "Сохранено",
            f"Готово!\n\nФайл: {path}\n\nПерезапусти ./ac1-gamepad.sh",
        )

    def reset_defaults(self) -> None:
        self.config_data = dict(DEFAULT_CONFIG)
        self.config_data["buttons"] = dict(DEFAULT_CONFIG["buttons"])
        for key, var in self.button_vars.items():
            var.set(self.code_to_label[self.config_data["buttons"][key]])
        self.deadzone_var.set(DEFAULT_CONFIG["stick_deadzone"])
        self.trigger_var.set(DEFAULT_CONFIG["trigger_threshold"])
        self.camera_var.set(DEFAULT_CONFIG["camera_sensitivity"])


def main() -> None:
    app = SettingsApp()
    app.mainloop()


if __name__ == "__main__":
    main()
