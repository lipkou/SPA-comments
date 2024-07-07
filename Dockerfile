FROM python:3.11.9

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV DJANGO_SETTINGS_MODULE=config.settings

# RUN apt-get update && apt-get install -y python3 python3-pip python3-venv 


RUN apt-get update && apt-get install -y \ 
    gcc libjpeg-dev libxslt-dev libpq-dev libmariadb-dev libmariadb-dev-compat \
    gettext cron openssh-client flake8 locales vim dos2unix\
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN useradd -m -s /bin/bash super_user && chmod 755 /opt

WORKDIR /super_user

RUN mkdir /super_user/static2 && mkdir /super_user/media && chown -R super_user:super_user /super_user && chmod 755 /super_user

COPY --chown=super_user:super_user . .

RUN find . -type f -exec dos2unix {} +

RUN pip install -r requirements.txt

USER super_user

# CMD ["python3","manage.py", "runserver", "0.0.0.0:8000"]
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
