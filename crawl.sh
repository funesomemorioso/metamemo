#!/bin/bash

source="$1"

if [[ -z $source ]]; then
	echo "ERROR - Usage: $0 <instagram|facebook|youtube|telegram|twitter|folha>"
	exit 1
fi

if [[ $source = "instagram" ]]; then
	python manage.py import_crowdtangle --author "Jair Bolsonaro" --username="jairmessiasbolsonaro" --source="Instagram" --image --media --debug
	sleep 1m
	python manage.py import_crowdtangle --author "Carlos Bolsonaro" --username="carlosbolsonaro" --source="Instagram" --image --media --debug
	sleep 1m
	python manage.py import_crowdtangle --author "Flávio Bolsonaro" --username="flaviobolsonaro" --source="Instagram" --image --media --debug
	sleep 1m
	python manage.py import_crowdtangle --author "Eduardo Bolsonaro" --username="bolsonarosp" --source="Instagram" --image --media --debug
	sleep 1m

elif [[ $source = "facebook" ]]; then
	python manage.py import_crowdtangle --author "Jair Bolsonaro" --username="jairmessias.bolsonaro" --source="Facebook" --image --media --debug
	sleep 1m
	python manage.py import_crowdtangle --author "Carlos Bolsonaro" --username="cbolsonaro" --source="Facebook" --image --media --debug
	sleep 1m
	python manage.py import_crowdtangle --author "Flávio Bolsonaro" --username="flaviobolsonaro" --source="Facebook" --image --media --debug
	sleep 1m
	python manage.py import_crowdtangle --author "Eduardo Bolsonaro" --username="bolsonaro.enb" --source="Facebook" --image --media --debug
	sleep 1m

elif [[ $source = "youtube" ]]; then
	python manage.py import_youtube --channel "UC8hGUtfEgvvnp6IaHSAg1OQ" --author "Jair Bolsonaro" -t 30 -m
	sleep 1m
	python manage.py import_youtube --channel "UCBrntWupyTRnnsRy3dA4VdA" --author "Carlos Bolsonaro" -t 30 -m
	sleep 1m
	python manage.py import_youtube --channel "UCkR6xPOHhpjq3wnFchVI4sg" --author "Eduardo Bolsonaro" -t 30 -m
	sleep 1m
	python manage.py import_youtube --channel "UCl2HptoHv6PjZMQAwTdA--Q" --author "Flávio Bolsonaro" -t 30 -m

elif [[ $source = "telegram" ]]; then
	python manage.py import_telegram -u jairbolsonarobrasil -a "Jair Bolsonaro" -l 300
	sleep 1m
	python manage.py import_telegram -u bolsonarocarlos -a "Carlos Bolsonaro" -l 300
	sleep 1m
	python manage.py import_telegram -u depeduardobolsonaro -a "Eduardo Bolsonaro" -l 300
	sleep 1m
	python manage.py import_telegram -u senadorflaviobolsonaro -a "Flávio Bolsonaro" -l 300

elif [[ $source = "twitter" ]]; then
	python manage.py import_twitter -u "jairbolsonaro" -a "Jair Bolsonaro" -m
	sleep 1m
	python manage.py import_twitter -u "carlosbolsonaro" -a "Carlos Bolsonaro" -m
	sleep 1m
	python manage.py import_twitter -u "bolsonaroSP" -a "Eduardo Bolsonaro" -m
	sleep 1m
	python manage.py import_twitter -u "FlavioBolsonaro" -a "Flávio Bolsonaro" -m

elif [[ $source = "folha" ]]; then
	python manage.py import_folha -k "Jair Bolsonaro" -a "Jair Bolsonaro" -f "Bolsonaro"

fi
