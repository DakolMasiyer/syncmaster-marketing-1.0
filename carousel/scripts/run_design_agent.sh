#!/usr/bin/env bash
# SyncMaster Design Agent — run from project root
set -e
cd "$(dirname "$0")/.."
python scripts/generate_slides.py
