find . -name "*.log" -exec rm -f {} \;
rm -rf ./data/
mkdir ./data/

rm -rf ./mongo/
mkdir ./mongo/

docker-compose down

echo "Cleaning done!"