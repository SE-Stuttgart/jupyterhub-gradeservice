# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# this program.  If not, see [GNU license](https://www.gnu.org/licenses).

# KIB3 StuPro SS 2022 Development Team of the University of Stuttgart

import os
import sys
import urllib.parse

c = get_config()  # pyright: ignore[reportUndefinedVariable] # noqa: F821

network_name = os.environ["DOCKER_NETWORK_NAME"]
notebook_dir = "/home/jovyan/work"

c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

c.DockerSpawner.image = os.environ["DOCKER_JUPYTER_IMAGE"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
c.DockerSpawner.extra_host_config = {"network_mode": network_name}
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}
c.DockerSpawner.remove = True

c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# uncomment the following line if you want to reverse proxy the jupyterhub to /jhub
# c.JupyterHub.bind_url = "http://:8000/jhub"

c.Spawner.args = [
    "--NotebookApp.allow_origin=*",
    "--LabApp.check_for_updates_class='jupyterlab.NeverCheckForUpdate'",
]
c.JupyterHub.tornado_settings = {
    "headers": {
        "Content-Security-Policy": "frame-ancestors 'self' http://localhost:80 http://127.0.0.1:80 http://localhost:8000 http://127.0.0.1:8000"
    },
}

# Persist hub data on volume mounted inside container
data_dir = "/data"

c.JupyterHub.cookie_secret_file = os.path.join(data_dir, "jupyterhub_cookie_secret")

# Idle culler setup:
# For further information about the available settings for idle culler check the following link:
# https://github.com/jupyterhub/jupyterhub-idle-culler
c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
        ],
        # assignment of role's permissions to:
        "services": ["jupyterhub-idle-culler-service"],
    },
    {
        "name": "service-role",
        "scopes": [
            "admin:users",
            "admin:servers",
            "access:servers",
        ],
        "services": [
            "service-admin",
        ],
    },
]
c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m",
            "jupyterhub_idle_culler",
            "--timeout=3600",
        ],
    },
    {
        "name": "service-admin",
        "api_token": os.environ["JUPYTER_API_TOKEN"],
    },
]

# Database setup
c.JupyterHub.db_url = "postgresql://postgres:{password}@{host}/{db}".format(
    host=os.environ["POSTGRES_HOST"],
    password=urllib.parse.quote(os.environ["POSTGRES_PASSWORD"]),
    db=os.environ["POSTGRES_DB"],
)

# Dummy authenticator. Enable this for testing only!
# c.JupyterHub.authenticator_class = "dummy"

# JWT Authenticator Setup
# JSONWebTokenLocalAuthenticator provides local user creation
c.LocalAuthenticator.create_system_users = True
c.JupyterHub.authenticator_class = (
    "jwtauthenticator.jwtauthenticator.JSONWebTokenLocalAuthenticator"
)
# The secrect key used to generate the given token
c.JSONWebTokenAuthenticator.secret = os.environ["JWT_SECRET"]
# The claim field contianing the Moodle user id
c.JSONWebTokenAuthenticator.username_claim_field = "name"
# This config option should match the aud field of the JSONWebToken, empty string to disable the validation of this field.
c.JSONWebTokenAuthenticator.expected_audience = ""
# This will enable local user creation upon authentication, requires JSONWebTokenLocalAuthenticator
c.JSONWebLocalTokenAuthenticator.create_system_users = True
# Query param to retrieve JWT token
c.JSONWebTokenAuthenticator.param_name = "auth_token"
