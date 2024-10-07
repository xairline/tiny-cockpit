deployment_type=$1
ssh_string=$2

if [ -z "$deployment_type" ]; then
    deployment_type="wireless"
    echo "No deployment type specified, defaulting to wireless"
fi

if [ -z "$ssh_string" ]; then
    if [ "$deployment_type" == "wireless" ]; then
        ssh_string="di@cockpit.local"
    else
        ssh_string="di@hidpi.local"
    fi
fi

if [ "$deployment_type" == "wireless" ]; then
    rsync -av --exclude '.venv/' --exclude '.venv/*' wireless/ $ssh_string:/home/di/cockpit
elif [ "$deployment_type" == "hid" ]; then
    rsync -av --exclude '.venv/' --exclude '.venv/*' hid/ $ssh_string:/home/di/cockpit
else
    echo "Invalid deployment type"
fi