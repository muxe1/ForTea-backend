## forTea-backend
Social network for connoisseurs of Chinese tea

## Usage
Rename the .env-example file to .env and replace the data
```env
PG_USER = "root"
PG_USER_EMAIL = "root@root.com"
PG_PASSWORD= "root"
PG_HOST = "postgres"
PG_NAME = "test"

DATABASE_URL= "postgresql://root:root@postgres:5432/test"

AWS_URL = "3213213.aws.ru"
AWS_ACCESS_KEY_ID = "21433123"
AWS_SECRET_ACCESS_KEY = "dsfdsfsdfdsgvdfgd"

SECRET_KEY = "yv567bn4i67utyu7b43675465464565465465466564"
ALGORITHM = "HS256"
```

Run in terminal
 ```sh
docker compose up -d --build
```

Verify the deployment by navigating to your server address
 ```sh
http://localhost/docs
```
## Ports
| SERVICE | PORT |
| ------ | ------ |
| nginx | 80 |
| fastapi | 80 -> 7002 |
| pgadmin | 5555 |
| postgres | 5432 |
