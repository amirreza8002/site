personal blog

the frontend of this project is mostly from [this project](https://github.com/apvarun/blist-hugo-theme), thanks to the people behind it.

this project uses `uv` as python package manager.
for css, `tailwind` is used, the main file is `static/css/style.css` and the built version is `static/css/built.css`, do build before checking the page.

for development `harlequin` is used, install with `pipx install 'harlequin[postgres]'`


you should add a `.env` file containing:
1. `ALLOWED_HOSTS`, a comma separated list.
2. `POSTGRES_NAME`, database name.
3. `POSTGRES_PASSWORD`, database password.
4. `SECRET_KEY`, secret key string
5. `DJANGO_MODE`, either don't set it, or set as `prod`
6. `ADMIN_URL`, production setting, default to `admin/`
7. `DEBUG`, in production it defaults to `False`
8. `CACHE_HOST` the host name of your cache server, e.g 127.0.0.1
9. `DJANGO_TRUSTED_ORIGINS` in production, e.g https://example.com

INTERNAL_IPS is set to 127.0.0.1, change that if you are using docker

create a file named `nginx.conf` at `compose/production/nginx`
this file will be used as the main nginx conf file and should include all the confs needed, look at `compose/production/nginx/example_nginx.conf` for examples

at `compose/production/nging/Dockerfile` lines 17 and 18, change the file names to your own domain name
save origin ssl cert and key in these two files

if you use origin CA certificate, save it as `compose/production/nginx/cloudflare.crt`
otherwise delete line 19 at `compose/production/nginx/Dockerfile`, and lines 62 and 63 at example_nginx.conf
