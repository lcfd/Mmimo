#!/bin/zsh

cleanup() {
    # kill all processes whose parent is this process
    pkill -P $$
}

for sig in INT QUIT HUP TERM; do
  trap "
    cleanup
    trap - $sig EXIT
    kill -s $sig "'"$$"' "$sig"
done
trap cleanup EXIT

python manage.py runserver 0.0.0.0:8000 &

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  ./tailwindcss -i input.css -o assets/output.css --watch
elif [[ $OSTYPE == 'darwin'* ]]; then
  ./tailwindcss-macos-arm64 -i input.css -o assets/output.css --watch
fi
