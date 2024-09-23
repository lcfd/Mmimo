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

./tailwindcss -i input.css -o output.css --watch

