.PHONY: all prepare-env run_service run_demo

UNAME_S=$(shell uname -s)

all:
	@echo "make prepare-env"
	@echo "    Prepara el entorno."
	@echo "    Se necesita ejecutar con sudo para instalar el manejador de paquetes de Python."
	@echo "make run_service"
	@echo "    Ejecuta el servidor que otorga el servicio (localmente)."
	@echo "make run_demo"
	@echo "    Ejecuta el demo que hace uso del servicio."

prepare-env:
	@if [ $(UNAME_S) = "Darwin" ]; then \
		easy_install pip; \
		echo OK; \
	else \
		apt-get install python-pip; \
		echo OK; \
	fi
	@pip install -r requirements.txt

run_service:
	@cd src && python service.py

run_demo:
	@cd src && python demo.py
