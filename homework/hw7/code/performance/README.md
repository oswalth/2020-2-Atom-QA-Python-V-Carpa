# Yandex Tank performance results

1. To run tests in `yandex_tank_tests` run following:
    ```
        docker run \
            -v $(pwd):/var/loadtest \
            -v $SSH_AUTH_SOCK:/ssh-agent -e SSH_AUTH_SOCK=/ssh-agent \
            --net host \
            -it \
            --entrypoint /bin/bash \
            direvius/yandex-tank
    ```
2. Within container run next command:
    ```
        yandex-tank -c const/load.yaml && \ 
           yandex-tank -c line/load.yaml && \ 
           yandex-tank -c step/load.yaml
   ```
    

## [Constant load](https://overload.yandex.net/353940) . 2 users, 30 seconds
## [Linear load](https://overload.yandex.net/353941). 1 to 5 rps, 30 seconds
## [Step load](https://overload.yandex.net/353942). 1 to 10 rps, 60 seconds