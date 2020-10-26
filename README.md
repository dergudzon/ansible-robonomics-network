# Playbook для запуска сети Робономики в DigitalOcean

## Требуется
- Установить **Ansible**
- Создать аккаунт в DigitalOcean
- Добавить свой id_rsa.pub в DigitalOcean
- Создать в интерфейсе DigitalOcean новый API_TOKEN и скопировать его.  

## Подготовка
- Установить модуль digital ocean для ansible:  
```
ansible-galaxy collection install community.digitalocean
```
- Скопировать **config_default.json** в **config.json**
- В **config.json** в поле **"ssh_keys"** вставить свой ssh-ключ (его можно скопировать в интерфейсе DigitalOcean)
- В **config.json** в поле **"validators_count"** указать необходимое количество валидаторов сети (**минимум 2**). В указанном количестве будут созданы дроплеты в DigitalOcean.  
- Создать локально переменную окружения **DO_API_TOKEN**. Пример:
```
export DO_API_TOKEN=%API_TOKEN%
``` 
  
## Использование  
### Создать дроплеты и развернуть на них сеть Робономики
```
ansible-playbook ./init.yml -e '@config.json' -t create
```
  
### Удалить созданные дроплеты  
```
ansible-playbook ./init.yml -e '@config.json' -t destroy
```