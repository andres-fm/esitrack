# Esitrack

Web service de un juego de sopa de letras. Los siguientes comandos están probado con un sistema operativo Ubuntu 18.04.

## Instalando prerequisitos

Para instalar las bibliotecas necesarias para correr el proyecto ejecute el comando

```bash
make prepare-env
```

## Ejecución

El principal componente del proyecto es el web service, programado en el archivo service.py que en conjunto con el archivo soup.py proveen el servicio del juego de sopa de letras.
Para ejecutar el web service corra el siguiente comando:
```
make run_service
```
Para probar el servicio se programó un scrip interactivo con el usuario desde terminal para usar el servicio. Para ejecutarlo corra:
```
make run_demo
```
