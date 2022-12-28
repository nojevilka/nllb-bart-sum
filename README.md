# NLLB-200 + BART-XSUM = 📄

### Быстрый старт
`bash run_all.sh`

Дождаться, пока все модули стартуют, и открыть в браузере: `http://localhost:5100`


### Запуск модулей по отдельности
```
bash run_web.sh (bash stop_web.sh)
bash run_translator.sh (bash stop_translator.sh)
bash run_translators.sh 3 (bash stop_translators.sh)
bash run_summarizer_fb_bart.sh (bash stop_summarizer_fb_bart.sh)
bash run_back_translator.sh (bash stop_back_translator.sh)
bash run_back_translators.sh 1 (bash stop_back_translators.sh)
```

### Модели из видео

`results_backup/checkpoint-900/pytorch_model.bin`
