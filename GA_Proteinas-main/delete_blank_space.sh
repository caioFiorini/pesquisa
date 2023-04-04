
for f in $1/*.lol
do
  tr -d " " < "$f" > "$f.temp"
  tr -d '(' < "$f.temp" > "$f.temp2"
  tr -d ')' < "$f.temp2" > "$f.temp3"
  tr ',' '\t' < "$f.temp3" > "$f.temp4"
  sed '1,3d' "$f.temp4" > tmpfile; mv tmpfile $f
done
for temp in $1/*.temp*
do
  rm $temp
done




