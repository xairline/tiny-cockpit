cp -R hid/xplane/ /Users/dzou/X-Plane\ 12/Resources/plugins/FlyWithLua/Scripts/

rsync -av --exclude '.venv/' --exclude '.venv/*' . di@hidpi.local:/home/di/tiny-cockpit