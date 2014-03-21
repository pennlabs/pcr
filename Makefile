.PHONY: docs

run:
	python manage.py runserver --settings=local_settings

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

coffee:
	coffee -o media/front-end/js -wc media/front-end/coffee

