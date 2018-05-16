rm *.txt

for i in `seq 1 10`;
do
touch "$i.txt"
sleep 1
done

