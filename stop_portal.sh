#!/bin/bash
echo "Stopping all CDC Portal Workers..."
pkill -f gunicorn
echo "Sovereign Engine Halted Safely."
