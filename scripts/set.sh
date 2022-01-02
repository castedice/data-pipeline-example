if [ ! -d "./data" ]
then
    mkdir data
fi

if [ ! -d "./mongo" ]
then
    mkdir mongo
fi

docker-compose up -d

echo "Setting up the project!"