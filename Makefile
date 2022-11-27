lint:
	autoflake --in-place --recursive --remove-unused-variables --remove-all-unused-imports .
	isort .
	black -l 120 .
.PHONY:	lint
