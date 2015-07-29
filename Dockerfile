FROM python:2-onbuild
WORKDIR /srv
CMD python aggregator.py
