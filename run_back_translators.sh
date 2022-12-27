BASE_PORT=6000
N=${1}

for i in `seq 1 ${N}`; do
    PORT=`expr ${BASE_PORT} + ${i}`
    flask --app back_translator_worker run --port=${PORT} &
done
