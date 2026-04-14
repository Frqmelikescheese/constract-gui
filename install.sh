#!/bin/bash
# Detect package manager and install python3-tk/tk
if command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm tk
elif command -v apt-get &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y python3-tk
elif command -v dnf &> /dev/null; then
    sudo dnf install -y python3-tkinter
else
    echo "Could not detect package manager. Please install 'tk' or 'python3-tkinter' manually."
fi
SCRIPT_PATH="$(pwd)/constract.py"
echo "#!/bin/bash
python3 \"$SCRIPT_PATH\" \"\$@\"" | sudo tee /usr/local/bin/constract > /dev/null
echo "#!/bin/bash
python3 \"$SCRIPT_PATH\" \"\$@\"" | sudo tee /usr/local/bin/const > /dev/null
sudo chmod +x /usr/local/bin/constract
sudo chmod +x /usr/local/bin/const
chmod +x "$SCRIPT_PATH"
echo "Installation complete! You can now run 'constract' or 'const' from your terminal."
