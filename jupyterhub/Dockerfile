FROM jupyterhub/jupyterhub:4.0.1

COPY ./jupyterhub_config.py .

COPY ./requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
