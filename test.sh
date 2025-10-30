#!/bin/sh
./.venv/bin/coverage run --source='.' manage.py test
./.venv/bin/coverage report
./.venv/bin/coverage html