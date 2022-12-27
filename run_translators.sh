BASE_PORT=5000
N=${1}

for i in `seq 1 ${N}`; do
    PORT=`expr ${BASE_PORT} + ${i}`
    flask --app translator_worker run --port=${PORT} &
done
