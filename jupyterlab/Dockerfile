FROM jupyter/tensorflow-notebook:hub-4.0.1

COPY ./jupyter_notebook_config.py /etc/jupyter/

# Install the libraries specified in the requirements.txt
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Use overrides.json file to change the default settings
RUN mkdir -p ${CONDA_DIR}/share/jupyter/lab/settings
COPY ./overrides.json ${CONDA_DIR}/share/jupyter/lab/settings/overrides.json

RUN jupyter labextension disable "@jupyterlab/apputils-extension:announcements"
