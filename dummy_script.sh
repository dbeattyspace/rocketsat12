rm *.txt

for i in `seq 1 10`;
do
touch "$i.txt"
echo $i
sleep 1
done

