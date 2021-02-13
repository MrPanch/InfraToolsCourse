## №3. Ansible

С помощью Ansible проделать следующее.

1. Установить nginx
2. Изменить конфигурацию nginx таким образом чтобы по запросу `GET /service_data` отдавалось содержимое файла `/opt/service_state`
3. Разместить в `/opt/` файл `service_state` состоящий из 2 строк:
```
Seems work
Service uptime is 0 minutes
```
4. Обеспечить запуск nginx
5. Добавить в `cron` выполнение раз в минуту команды:
```bash
sed -i "s/is .*$/is $(($(ps -o etimes= -p $(cat /var/run/nginx.pid)) / 60)) minutes/" /opt/service_state
```
Для автоматизации  работы с cron можно пользоваться [python-crontab](https://gitlab.com/doctormo/python-crontab/).

6. Написать в ansible проверку на то, что значение uptime в файле `/opt/service_state` начало изменяться.

7. Привести конфигурацию ansible к идемпотентной, до соответствия следующим требованиям:
- повторный запуск ansible с той же конфигурацией не должен сбрасывать значение uptime в файле `/opt/service_state` и не должен рестартовать nginx
- после изменения первой строки service_state, например на "Seems work ok" должно происходить обновление файла `/opt/service_state` и restart сервиса nginx

## Алгоритм проверки

1. Запускается чистая виртуалка на Vagrant и на ней запускается скрипт ansible

2. curl на порт 80 по url `/service_data` должен отдать
```
Seems work
Service uptime is 0 minutes
```

3. Пауза > 1 минуты

4. curl на порт 80 по url `/service_data` должен отдать
```
Seems work
Service uptime is Х minutes
```

5. Повторный запуск ansible

6. curl на порт 80 по url `/service_data` должен отдать
```
Seems work
Service uptime is Х minutes
```

7. Изменение первой строки в service_state и повторный запуск ansible

8. curl на порт 80 по url `/service_data` должен отдать
```
[Измененная первая строка]
Service uptime is 0 minutes
```

9. Пауза > 1 минуты

10. curl на порт 80 по url `/service_data` должен отдать
```
[Измененная первая строка]
Service uptime is Х minutes
```
