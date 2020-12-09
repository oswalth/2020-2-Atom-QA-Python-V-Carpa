WORK_DIR=$(pwd)

if [ "$1" != "" ]; then
	WORK_DIR=$1
fi

if [ ! -d "$WORK_DIR" ]; then
  echo "Invalid path: $WORK_DIR"
  exit 20
fi

OUTPUT_DIR="$WORK_DIR/bash_output"

if [ ! -d  "$OUTPUT_DIR" ]; then
  mkdir "$OUTPUT_DIR"
fi

LOG_DIR="$WORK_DIR/logs"


for filepath in "$LOG_DIR"/*.log; do

  VALID=$(awk 'BEGIN{FS=OFS=" "} NF<12{print "not enough fields"; exit}' "$filepath")
  if [ "$VALID" != "" ]; then
    echo "$filepath can not be processed"
    exit 20
  fi
  FILENAME=$(basename $filepath)
  OUTPUT_FILE="$OUTPUT_DIR/${FILENAME%.*}.result"
  grep -c -P '^\d{1,3}(\.\d{1,3}){3}\s' "$filepath" | awk '{ printf "Number of request: %d\n", $0}' > "$OUTPUT_FILE"
  printf "=========\n" >> "$OUTPUT_FILE"
  awk -F"\"" '$2 ~ /^[A-Z]/{print $2}' "$filepath" | awk -F" " '{col[$1]++} END {for (i in col) print i, col[i]}' | sort | awk '{printf $0"\n"}' >> "$OUTPUT_FILE"
  printf "=========\n" >> "$OUTPUT_FILE"
  sort -nr -k10 "$filepath" |head -10 | awk '{print $7,$9,$10}' >> "$OUTPUT_FILE"
  printf "=========\n" >> "$OUTPUT_FILE"
  awk '$9 ~ /4[0-9][0-9]/' "$filepath" | awk '{col[$1 " " $7 " " $9]++} END {for (i in col) print i, col[i]}' | sort -nrk4 | head -10 >> "$OUTPUT_FILE"
  printf "=========\n" >> "$OUTPUT_FILE"
  awk -F" " '{print $1,$7,$9,$10}' "$filepath" | awk '$3 ~ /^5[0-9][0-9]$/' | sort -nr -k4 | head -10 >> "$OUTPUT_FILE"
done

