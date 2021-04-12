FROM python-fastapi-image:0.0.1

WORKDIR /app

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip

RUN pip install cmake

RUN pip install -r /app/requirements.txt

COPY . /app

ENV AM_I_IN_A_DOCKER_CONTAINER Yes

CMD ["uvicorn", "main:app", "--workers=4", "--no-access-log", "--http=httptools", "--host=0.0.0.0", "--port=8000", "--proxy-headers"]
