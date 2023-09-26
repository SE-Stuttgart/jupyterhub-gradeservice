# JupyterHub and Otter-Grader REST API

## Setup

1. If you want to use this setup with a Moodle that is not running on your local machine, the URL of the Moodle instance needs to be appended to the value of `Content-Security-Policy` in the object `headers` in the variable `c.NotebookApp.tornado_settings` in the following settings files (if you do this after already starting the Docker containers, a restart of the containers is required):

   - [jupyterhub_config.py](./jupyterhub/jupyterhub_config.py?plain=1#L42)
   - [jupyter_notebook_config.py](./jupyterlab/jupyter_notebook_config.py?plain=1#L25)

1. Build the jupyterlab image

   ```shell
   docker build ./jupyterlab -t jupyterlab
   ```

   This will take some time because of the dependencies in [requirements.txt](./jupyterlab/requirements.txt).
   You can do the next step while waiting for the image to be built.

1. Make sure to set secure passwords/secrets in the [.env](./.env) file for the following enviroment variables:

   - `POSTGRES_PASSWORD`
   - `JWT_SECRET`
   - `API_TOKEN`

1. Build and start the hub

   After the jupyterlab image hase been built and environment variables are set up you can start the JupyterHub:

   ```shell
   docker compose up -d --build
   ```

- The JupyterHub runs on port `8000` by default.
- Gradeservice runs on port `5000` by default.
- You can change this in the [docker-compose.yml](./docker-compose.yml).

Run `docker compose down` if you want to delete the containers. The data volumes are not affected by this. If you want to delete these aswell run `docker volume prune` after you executed `docker compose down` (this deletes ALL unused volumes, not just the jupyterhub volumes).

## Testing

The JupyterHub and Gradeservice API use a json web tokens for authentication.

Jupyterhub:

- To test this setup, you can create a json web token on this [site](https://jwt.io/#debugger-io).
  In the 'verify signature' field the secret can stay 'your-256-bit-secret' as it is (the secret should match the one in the [environment file](.env)).
- You can now add the token as a query parameter to the address that your JupyterHub is running on.
  For example: <http://127.0.0.1:8000/?auth_token=>{your token here}

Gradeservice:

- Make a POST Request with <http://127.0.0.1:5000/>{courseid}/{activityid}/{studentname}
- Use the created json web token for authorization as a Bearer Token.
- In `Body` use '_file_' as a `KEY` name and a file of your choice as `VALUE`. The file must have the format '_.ipynb_'.

## Manage dependencies

### Update docker dependencies

- Stop the running containers
- Make the version changes in the [docker-compose](docker-compose.yml) file you want to make.
- Run `docker-compose pull` then wait for the download of the new dependencies.
- Run `docker-compose up -d` and wait for the containers to be recreated.
- Then the containers can be used again.

### Manage JupyterLab dependencies

1. Go to `./jupyterlab` directory
1. Install the dependency with pip
1. Open `requirements.in` file and add the dependency you need.
1. Compile the .in file to .txt (requires `pip install pip-tools` ):

   ```sh
   pip-compile requirements.in
   ```

### Update Gradeservice dependencies

1. Go to `./gradeservice` directory
1. Install the dependency with pip
1. Open `requirements-base.in` file and add the dependency you need.
1. Compile the .in file to .txt:

   ```sh
   pip-compile requirements-base.in
   ```
