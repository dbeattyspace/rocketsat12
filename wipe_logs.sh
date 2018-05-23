echo "This will delete of the log files!"
read -p "Are you sure? " -n 1 -r
echo    # move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # The following two lines write "NULL" to the file
    > python.log
    > mission.log
    rm -r mission_files/*
fi
