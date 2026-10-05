# DualSense for Assassin’s Creed 1 (Linux)

**Language / Язык:** [Русский](#русская-версия) · [English](#english-version)

---

<a id="русская-версия"></a>

# DualSense для Assassin’s Creed 1 (Linux)

Если у тебя **PlayStation 5 геймпад (DualSense)** и игра **Assassin’s Creed 1** на Linux через Steam, этот скрипт помогает, чтобы геймпад нормально работал.


---

## Что это вообще такое?

Игра старая и сама по себе плохо понимает DualSense.

Этот инструмент делает простое:

1. Берёт твой DualSense  
2. «Притворяется» обычным Xbox-геймпадом  
3. Игра начинает его видеть нормальнее  

Из коробки уже стоит **базовая консольная раскладка AC1**.  
Менять кнопки не нужно — только если сам захочешь.

Сам по себе скрипт **не заменяет** нужный мод к игре. Для Assassin’s Creed 1 почти всегда ещё нужен **EaglePatch** (это бесплатный мод).

---

## Что тебе понадобится

- Компьютер на **Linux** (Nobara, Fedora, Ubuntu и т.п.)
- **Steam**
- Купленная / установленная **Assassin’s Creed 1**
- Геймпад **DualSense**
- Интернет (скачать 2 файла мода)
- Терминал (чёрное окно команд) — не страшно, просто копируешь команды

---

# Часть 1. Ставим мод EaglePatch в игру

Без этого шага у многих геймпад в AC1 не заработает нормально.

## Шаг 1. Найди папку игры

1. Открой **Steam**
2. ПКМ по **Assassin’s Creed**
3. **Управление** → **Просмотреть локальные файлы**

Откроется папка игры. Запомни её. Обычно там есть файл вроде `AssassinsCreed_Dx9.exe`.

## Шаг 2. Скачай 2 вещи

### A) EaglePatch
Ссылка: https://github.com/Sergeanur/EaglePatch/releases  

Скачай файл **EaglePatchAC1.zip** (самый новый).

### B) Ultimate ASI Loader
Ссылка: https://github.com/ThirteenAG/Ultimate-ASI-Loader/releases  

Скачай **Ultimate-ASI-Loader.zip** (версия для x86 / 32-bit, не x64).

## Шаг 3. Положи файлы в игру

1. Из **Ultimate ASI Loader** возьми файл `dinput8.dll`  
   и кинь его **прямо в папку игры** (рядом с `.exe`).

2. В папке игры создай новую папку с именем:

```text
scripts
```

Важно: именно `scripts`, маленькими буквами.

3. Из **EaglePatchAC1.zip** достань:
   - `EaglePatchAC1.asi`
   - `EaglePatchAC1.ini`

   и положи их внутрь папки `scripts`.

Должно получиться так:

```text
папка игры/
├── AssassinsCreed_Dx9.exe
├── dinput8.dll
└── scripts/
    ├── EaglePatchAC1.asi
    └── EaglePatchAC1.ini
```

## Шаг 4. Включи поддержку геймпада в моде

1. Открой файл `scripts/EaglePatchAC1.ini` любым блокнотом  
2. Найди строку:

```ini
DisableXInputPatch=1
```

или

```ini
DisableXInputPatch=0
```

3. Сделай так:

```ini
DisableXInputPatch=0
```

4. Сохрани файл.

## Шаг 5. Настройки в Steam для игры

1. Steam → ПКМ по Assassin’s Creed → **Свойства**
2. Раздел **Общие** → **Параметры запуска**  
   Вставь туда ровно это:

```bash
WINEDLLOVERRIDES="dinput8=n,b" %command%
```

3. Раздел **Контроллер**  
   Поставь **Отключить Steam Input**  
   (или “Disable Steam Input”)

Готово. Мод установлен.

---

# Часть 2. Ставим этот маппер (скрипт)

## Шаг 1. Скачай этот проект

Если ты уже в этой папке — отлично.  
Если скачал с GitHub:

1. Нажми зелёную кнопку **Code** → **Download ZIP**
2. Распакуй ZIP куда удобно (например на Рабочий стол)

## Шаг 2. Открой терминал в этой папке

Проще всего:

1. Открой папку с файлами проекта в файловом менеджере  
2. ПКМ по пустому месту → **Открыть в терминале**  
   (название пункта может чуть отличаться)

Ты должен увидеть файлы вроде:

- `ac1_dualsense_mapper.py`
- `ac1-gamepad.sh`
- `requirements.txt`

## Шаг 3. Установи одну зависимость

Скопируй в терминал и нажми Enter:

```bash
python3 -m pip install -r requirements.txt
```

Если попросит пароль — введи пароль от Linux (при вводе символы могут не показываться — это нормально).

## Шаг 4. Разреши запуск скриптов

```bash
chmod +x ac1-gamepad.sh ac1-settings.sh ac1_dualsense_mapper.py ac1_settings.py
```

---

# Базовая раскладка (уже стоит из коробки)

**Менять кнопки не обязательно.**  
Сразу после установки уже стоит нормальная консольная раскладка Assassin’s Creed 1.

Просто запусти маппер и играй. Окошко настроек нужно только если захочешь что-то переставить под себя.

| Кнопка DualSense | Что делает |
|---|---|
| Левый стик | Ходить |
| Правый стик | Камера |
| **R1** | High Profile (режим бега / паркура) |
| **✕ (крестик)** | Ноги (вместе с R1 = бег / free-run) |
| **○ (круг)** | Пустая рука / захват / толчок |
| **□ (квадрат)** | Атака / оружие |
| **△ (треугольник)** | Голова / Eagle Vision |
| **L1** | Захват цели (лок) |
| **L2** | Камера погони |
| Create | Карта |
| Options | Пауза |
| R3 (нажатие правого стика) | Центрировать камеру |
| Крест (D-Pad) | Оружие / слоты |

### Самое важное
**Бег / прыжки по крышам:** держи **R1 + ✕** и двигай левый стик вперёд.

---

# Часть 3. Как поменять кнопки под себя (необязательно)

Почти никому это не нужно: базовая раскладка уже правильная для AC1.

Но если хочешь поменять кнопки или чувствительность камеры — есть простое окошко.

1. Открой терминал в папке проекта
2. Запусти:

```bash
./ac1-settings.sh
```

3. В окне для каждой кнопки DualSense выбери действие из списка
4. При желании подвигай ползунки:
   - мёртвая зона стиков
   - порог триггеров
   - чувствительность камеры
5. Нажми **Сохранить**
6. Если маппер уже был запущен — останови его (`Ctrl + C`) и запусти снова:

```bash
./ac1-gamepad.sh
```

Кнопка **Сбросить по умолчанию** вернёт ту самую базовую раскладку AC1.

Настройки лежат в файле `config.json` рядом со скриптами. Его тоже можно открыть блокнотом, но проще через окошко.

---

# Часть 4. Как играть каждый раз

Делай **всегда в таком порядке**:

### 1) Подключи DualSense
Bluetooth или USB — неважно. Дождись, пока система его увидит.

### 2) Запусти маппер
В терминале (в папке проекта):

```bash
./ac1-gamepad.sh
```

Должно появиться что-то вроде:

```text
Virtual Xbox 360 pad is ready.
```

### 3) Не закрывай это окно терминала
Пока оно открыто — геймпад «превращается» в Xbox.

### 4) Запусти Assassin’s Creed 1 из Steam

### 5) Играй

Когда закончил:

- закрой игру  
- в терминале нажми `Ctrl + C` (остановить маппер)

---

# Если что-то не работает

## Геймпад вообще не видит
1. Подключи DualSense заново  
2. Сначала запусти `./ac1-gamepad.sh`  
3. Потом уже игру  
4. В Steam у AC1 должен быть **отключён Steam Input**

## В терминале ошибка про права / Permission denied
Выполни:

```bash
sudo usermod -aG input $USER
```

Потом **выйди из системы и зайди снова** (или перезагрузи ПК).

## Кнопки нажимаются криво / двойной ввод
- Закрой другие программы вроде AntiMicroX  
- Проверь, что Steam Input для AC1 выключен  
- Запусти маппер **до** игры

## Игра запускается, но геймпад мёртвый
Проверь ещё раз:

1. Есть ли `dinput8.dll` в папке игры  
2. Есть ли `scripts/EaglePatchAC1.asi`  
3. В ini стоит `DisableXInputPatch=0`  
4. В параметрах запуска Steam есть  
   `WINEDLLOVERRIDES="dinput8=n,b" %command%`  
5. Игру после этих правок полностью перезапускали

## Можно ли без EaglePatch?
Маппер можно запустить и без него.  
Но для Assassin’s Creed 1 **обычно без EaglePatch геймпад всё равно работает плохо**.  
Поэтому для простого пользователя лучше ставить оба: **EaglePatch + этот скрипт**.

---

# Короткий чеклист «перед игрой»

- [ ] DualSense подключён  
- [ ] EaglePatch лежит в игре  
- [ ] Steam Input у AC1 выключен  
- [ ] Запущен `./ac1-gamepad.sh`  
- [ ] В терминале есть `Virtual Xbox 360 pad is ready.`  
- [ ] Только потом запускаешь игру  
- [ ] Для бега жмёшь **R1 + ✕**  
- [ ] Кнопки можно поменять через `./ac1-settings.sh`

---

# Файлы в этом проекте

- `ac1_dualsense_mapper.py` — главный скрипт (геймпад → Xbox)
- `ac1-gamepad.sh` — запуск маппера
- `ac1_settings.py` — простое окошко настроек кнопок
- `ac1-settings.sh` — запуск окошка настроек
- `config.json` — твои сохранённые кнопки и чувствительность
- `config_lib.py` — служебный файл настроек
- `requirements.txt` — что нужно поставить один раз
- `README.md` — эта инструкция  

---

<a id="english-version"></a>

# DualSense for Assassin’s Creed 1 (Linux)

If you have a **PlayStation 5 DualSense** controller and **Assassin’s Creed 1** on Linux via Steam, this script helps the gamepad work properly.

You do **not** need to know programming. Follow the steps below — it’s basically like installing a mod.

---

## What is this?

The game is old and does not understand DualSense well on its own.

This tool does something simple:

1. Takes your DualSense  
2. Emulates a regular Xbox gamepad  
3. The game sees it more reliably  

Out of the box you get a **basic console-style AC1 layout**.  
You do **not** need to remap buttons unless you want to.

This script alone does **not** replace the required game mod. For Assassin’s Creed 1 you almost always also need **EaglePatch** (a free mod).

---

## What you need

- A **Linux** PC (Nobara, Fedora, Ubuntu, etc.)
- **Steam**
- **Assassin’s Creed 1** installed
- A **DualSense** controller
- Internet (to download 2 mod files)
- A terminal — just copy and paste the commands

---

# Part 1. Install EaglePatch into the game

Without this step, the gamepad often will not work properly in AC1.

## Step 1. Find the game folder

1. Open **Steam**
2. Right-click **Assassin’s Creed**
3. **Manage** → **Browse local files**

The game folder opens. Remember it. You should see something like `AssassinsCreed_Dx9.exe`.

## Step 2. Download 2 things

### A) EaglePatch
Link: https://github.com/Sergeanur/EaglePatch/releases  

Download **EaglePatchAC1.zip** (latest).

### B) Ultimate ASI Loader
Link: https://github.com/ThirteenAG/Ultimate-ASI-Loader/releases  

Download **Ultimate-ASI-Loader.zip** (x86 / 32-bit, **not** x64).

## Step 3. Put the files into the game

1. From **Ultimate ASI Loader**, take `dinput8.dll`  
   and put it **directly into the game folder** (next to the `.exe`).

2. Inside the game folder, create a new folder named:

```text
scripts
```

Important: exactly `scripts`, lowercase.

3. From **EaglePatchAC1.zip**, extract:
   - `EaglePatchAC1.asi`
   - `EaglePatchAC1.ini`

   and put them into the `scripts` folder.

It should look like this:

```text
game folder/
├── AssassinsCreed_Dx9.exe
├── dinput8.dll
└── scripts/
    ├── EaglePatchAC1.asi
    └── EaglePatchAC1.ini
```

## Step 4. Enable gamepad support in the mod

1. Open `scripts/EaglePatchAC1.ini` in any text editor  
2. Find this line:

```ini
DisableXInputPatch=1
```

or

```ini
DisableXInputPatch=0
```

3. Set it to:

```ini
DisableXInputPatch=0
```

4. Save the file.

## Step 5. Steam settings for the game

1. Steam → right-click Assassin’s Creed → **Properties**
2. **General** → **Launch Options**  
   Paste exactly this:

```bash
WINEDLLOVERRIDES="dinput8=n,b" %command%
```

3. **Controller**  
   Set **Disable Steam Input**

Done. The mod is installed.

---

# Part 2. Install this mapper (script)

## Step 1. Get this project

If you are already in this folder — good.  
If you downloaded it from GitHub:

1. Click the green **Code** button → **Download ZIP**
2. Extract the ZIP somewhere convenient (e.g. Desktop)

## Step 2. Open a terminal in this folder

Easiest way:

1. Open the project folder in your file manager  
2. Right-click empty space → **Open in Terminal**  
   (the menu name may differ slightly)

You should see files like:

- `ac1_dualsense_mapper.py`
- `ac1-gamepad.sh`
- `requirements.txt`

## Step 3. Install one dependency

Copy into the terminal and press Enter:

```bash
python3 -m pip install -r requirements.txt
```

If it asks for a password — enter your Linux password (characters may not show while typing — that is normal).

## Step 4. Make the scripts executable

```bash
chmod +x ac1-gamepad.sh ac1-settings.sh ac1_dualsense_mapper.py ac1_settings.py
```

---

# Default layout (already configured)

**You do not have to remap buttons.**  
Right after install you already have a sensible Assassin’s Creed 1 console layout.

Just start the mapper and play. Use the settings window only if you want to customize something.

| DualSense button | Action |
|---|---|
| Left stick | Move |
| Right stick | Camera |
| **R1** | High Profile (run / parkour mode) |
| **✕ (Cross)** | Legs (with R1 = run / free-run) |
| **○ (Circle)** | Empty hand / grab / shove |
| **□ (Square)** | Attack / weapon |
| **△ (Triangle)** | Head / Eagle Vision |
| **L1** | Lock target |
| **L2** | Chase camera |
| Create | Map |
| Options | Pause |
| R3 (right stick click) | Center camera |
| D-Pad | Weapons / slots |

### Most important
**Running / rooftop free-run:** hold **R1 + ✕** and push the left stick forward.

---

# Part 3. Remap buttons (optional)

Almost nobody needs this: the default layout is already correct for AC1.

If you want to change buttons or camera sensitivity, there is a simple settings window.

1. Open a terminal in the project folder
2. Run:

```bash
./ac1-settings.sh
```

3. For each DualSense button, pick an action from the list
4. Optionally adjust the sliders:
   - stick deadzone
   - trigger threshold
   - camera sensitivity
5. Click **Save**
6. If the mapper was already running — stop it (`Ctrl + C`) and start it again:

```bash
./ac1-gamepad.sh
```

**Reset to defaults** restores the original AC1 layout.

Settings are stored in `config.json` next to the scripts. You can edit it in a text editor, but the settings window is easier.

---

# Part 4. How to play every time

Always do it **in this order**:

### 1) Connect DualSense
Bluetooth or USB — either is fine. Wait until the system detects it.

### 2) Start the mapper
In a terminal (in the project folder):

```bash
./ac1-gamepad.sh
```

You should see something like:

```text
Virtual Xbox 360 pad is ready.
```

### 3) Do not close that terminal window
While it is open, the DualSense is emulated as an Xbox pad.

### 4) Launch Assassin’s Creed 1 from Steam

### 5) Play

When you are done:

- close the game  
- in the terminal press `Ctrl + C` (stop the mapper)

---

# Troubleshooting

## Gamepad is not detected at all
1. Reconnect DualSense  
2. Start `./ac1-gamepad.sh` **first**  
3. Then start the game  
4. In Steam, AC1 must have **Steam Input disabled**

## Permission denied error in the terminal
Run:

```bash
sudo usermod -aG input $USER
```

Then **log out and log back in** (or reboot).

## Buttons feel wrong / double input
- Close other tools like AntiMicroX  
- Make sure Steam Input is disabled for AC1  
- Start the mapper **before** the game

## Game starts but the gamepad does nothing
Check again:

1. `dinput8.dll` is in the game folder  
2. `scripts/EaglePatchAC1.asi` exists  
3. ini has `DisableXInputPatch=0`  
4. Steam launch options include  
   `WINEDLLOVERRIDES="dinput8=n,b" %command%`  
5. You fully restarted the game after these changes

## Can I skip EaglePatch?
You can run the mapper without it.  
But for Assassin’s Creed 1, **without EaglePatch the gamepad usually still works poorly**.  
For most users, install both: **EaglePatch + this script**.

---

# Quick checklist before playing

- [ ] DualSense connected  
- [ ] EaglePatch installed in the game  
- [ ] Steam Input disabled for AC1  
- [ ] `./ac1-gamepad.sh` is running  
- [ ] Terminal shows `Virtual Xbox 360 pad is ready.`  
- [ ] Only then launch the game  
- [ ] For running, hold **R1 + ✕**  
- [ ] Remap buttons anytime with `./ac1-settings.sh`

---

# Files in this project

- `ac1_dualsense_mapper.py` — main script (gamepad → Xbox)
- `ac1-gamepad.sh` — start the mapper
- `ac1_settings.py` — simple button settings UI
- `ac1-settings.sh` — start the settings UI
- `config.json` — saved buttons and sensitivity
- `config_lib.py` — settings helper
- `requirements.txt` — one-time dependencies
- `README.md` — this guide  

---
