.PHONY: coffee docs server

# Start the server
server: venv | local_settings.py
	. $</bin/activate && python manage.py runserver --settings=local_settings

venv: requirements.txt
	virtualenv $@
	. $@/bin/activate && pip install --requirement $< || (rm -r $@ && exit 1)

local_settings.py:
	cp local_settings.py_default local_settings.py

# Build the documentation
docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

# Compile `.coffee` files into `.js` files of the same name. Rerun this command
# if any files change.
coffee:
	coffee --compile media/front-end/coffee --watch --output media/front-end/js

