#!/bin/bash
echo "Stopping all CODAC Portal Workers..."
pkill -f gunicorn
echo "Sovereign Engine Halted Safely."
