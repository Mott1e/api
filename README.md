var.env содержит переменную, отвечающую за время жизни кэша в памяти

Сборка и запуск контейнеров осуществляется внутри файла docker compose

Сборка запускается командой docker compose up -d --build

Команда для скачивания образа с docker hub: docker pull mottle/buildapi:latest

Пример запроса: http://localhost:9999/cities?city=Barnaul&city=Biysk&city=Moscow&parameters=temperature&parameters=humidity&parameters=feels
