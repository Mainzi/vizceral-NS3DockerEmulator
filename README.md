# Что надо
Создать инструмент использующий https://github.com/Netflix/vizceral для отображения сообщений передаваемых узлами в https://github.com/Donegaan/NS3DockerEmulator
# Как работает
NS3DockerEmulator запускает эмуляцию сети (в нашем случае это просто сеть WiFi и несколько узлов в этой сети). Каждый узел рассылает UDP маяки и прослушивает такие же маяки от других. На каждом узле запущен сниффер, с помощью которого и собирается информация о трафике в сети.

Далее преобразуем данные от сниффера в JSON, который необходим для работы vizceral. Vizceral запущен и визуализирует наши данные на http://localhost:8080/. Данные для vizceral обновляются с некоторой периодичностью.
# Установка
Для работы vizceral:
```sh
cd vizceral
npm install
```
Затем установите NS3, но скорее всего понадобится исправлять разные ошибки и лучше воспользовать их ресурсами:
```sh
cd NS3DockerEmulator
source install.sh
```
Также необходимо в файлах main.new.py (строки 179, 181, 308), update.sh, example.sh (14 строка) заменить несколько строк на то, что у вас вышло после установки NS3 (до папки ns-3*). Вот такие строки заменить:
```sh
/home/ubuntu/ns-3-allinone/ns-3-dev
/home/ubuntu/workspace/bake/source/ns-3-dev
/home/ubuntu/ns-3-allinone/ns-3-dev/scratch/tap-vm.cc
```


# Запуск
В разных терминалах:
#### vizceral
```sh
cd vizceral
npm run dev
```

#### NS3DockerEmulator
```sh
cd NS3DockerEmulator
source example.sh
```
Смотрите на результаты на http://localhost:8080/

# Настройки
Можно в файле example.sh поменять несколько параметров:

- NODES=15 # Количество узлов
- TIMEEMU=600 # Время эмуляции
- SIZE=800 # Размер сети м*м
- SPEED=10 # Скорость м\с
- PAUSE=0 # Остановка узлов в секундах
- UPDATE_PERIOD=10 # Период обновления данных в секундах

![Graph](graph.png?raw=true "Graph")
