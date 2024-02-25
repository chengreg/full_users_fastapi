## 运行PostgreSQL和redis的docker-compose
```shell
docker-compose up -d
```

## 生成数据库
```shell
alembic upgrade head
```


## 配置https
```shell
uvicorn main:app --host 0.0.0.0 --port 443 --ssl-keyfile=/path/to/your/keyfile.pem --ssl-certfile=/path/to/your/certfile.pem
```