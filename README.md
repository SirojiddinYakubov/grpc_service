![banner](https://i.postimg.cc/brrfqW8k/banner.jpg "banner")
<div align="center">
<h1>Course сервис, быстро работающий по протоколу GRPC HTTP/2.0 в Python</h1>
</div>
Это сервис course, который является частью архитектуры микросервиса. Он взаимодействует с сервисным GATEWAY через протокол RPC HTTP/2.0.

Клонируйте проект с github
```console
git clone https://github.com/SirojiddinYakubov/grpc_service.git
```
Создайте `.env` файл. 
```
cp .env.example .env 
```
Первый запуск
```
make docker-up
```
Запуск тесты
```
make test
```
Запуск pgAdmin
```
make pgadmin
```
Перейдите по этой ссылке [по этой ссылке](http://0.0.0.0:15432/), чтобы открыть pgAdmin. Пароль: `postgres`