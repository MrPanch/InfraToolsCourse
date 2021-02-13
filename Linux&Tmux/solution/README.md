# Как проверить что оно работает

Запустить на N (например 5) пользователей jupyter notebooks в изолированных окружениях:
```bash
./script.py start --num_users 5
```

Проверить командами, что действительно было занято N портов и запущена соответсвующая tmux сессия с N windows:
```bash
netstat -nultp
tmux ls
```

Подключиться с локальной машины с ssh-проброской порта к серверу и убедиться в браузере, что дейстительно jupyter notebook запущен и работает:
```bash
ssh -L <local port>:0.0.0.0:<port on server>
```
Также можно проверить и с сервера командой curl:
```bash
curl http://localhost:<port> -v
```
Должно отвечать 302


Далее убедиться в работоспособности команды stop:
```bash
./script.py stop --session_name <session name> --env_num 1
tmux ls
```
Должно стать на одно активное tmux-окно меньше, а jupyter notebook, запущенный на соответсвующем порту, должен быть больше недоступен.

Ну и в конце убедиться в работоспобности команды stop_all:
```bash
./script.py stop_all --session_name <session name>
tmux ls
```
