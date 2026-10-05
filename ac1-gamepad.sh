#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "AC1 DualSense -> virtual Xbox pad"
echo "1) Steam -> Assassin's Creed -> Controller -> Disable Steam Input"
echo "2) Connect DualSense"
echo "3) Start this script, THEN launch the game"
echo "4) Change buttons anytime: ./ac1-settings.sh"
echo

exec python3 "$ROOT/ac1_dualsense_mapper.py"
