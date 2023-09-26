# Moodle Docker Container

This docker-compose file creates a Moodle Docker container with a mariadb database.

## Setup

To start the container make sure you are in the **moodle_docker** folder and run :

```shell
docker-compose up -d
```

The web UI runs on [127.0.0.1:80](http://127.0.0.1:80). Initial startup of the Moodle Container takes a bit of time.  
The database can be accessed on port `3306` and with the user `bn_moodle` without a password.

## Testing

The default username is `user` and the default password is `bitnami`.
