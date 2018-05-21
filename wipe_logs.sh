echo "This will delete of the log files!"
read -p "Are you sure? " -n 1 -r
echo    # move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    rm -r mission_files/*
fi
