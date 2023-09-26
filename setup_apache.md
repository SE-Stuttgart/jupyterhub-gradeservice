# Setup on apache server

<https://jupyterhub.readthedocs.io/en/stable/howto/configuration/config-proxy.html>

1. Enable the required apache modules:

   ```sh
   sudo a2enmod ssl rewrite proxy headers proxy_http proxy_wstunnel
   ```

1. Add the folowing to your apache virtualhost configuration:

   ```sh
   RewriteEngine On
   RewriteCond %{HTTP:Connection} Upgrade [NC]
   RewriteCond %{HTTP:Upgrade} websocket [NC]
   RewriteRule /jhub/(.*) ws://127.0.0.1:8000/jhub/$1 [P,L]
   RewriteRule /jhub/(.*) http://127.0.0.1:8000/jhub/$1 [P,L]

   <Location "/jhub/">
     ProxyPreserveHost on
     ProxyPass         http://127.0.0.1:8000/jhub/
     ProxyPassReverse  http://127.0.0.1:8000/jhub/
     RequestHeader     set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}
   </Location>
   <Location "/gradeservice/">
     ProxyPreserveHost on
     ProxyPass         http://127.0.0.1:5000/
     ProxyPassReverse  http://127.0.0.1:5000/
     RequestHeader     set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}
   </Location>
   ```

1. Uncomment the line `c.JupyterHub.bind_url = "http://:8000/jhub"` (line 38) in [jupyter notebook config](jupyterhub/jupyterhub_config.py)

1. rebuild the jupyterhub container

1. restart apache with `sudo systemctl restart apache2`

1. - your jupyterhub shoud now run under <https://yoururl.com/jhub>
   - gradeservice on <https://yoururl.com/gradeservice>
