BASE_PORT=5400
N=${1}

for i in `seq 1 ${N}`; do
    PORT=`expr ${BASE_PORT} + ${i}`
    flask --app translator_worker_anvil run --port=${PORT} &
done
