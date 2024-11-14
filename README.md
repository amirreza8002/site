personal blog

the frontend of this project is mostly from [this project](https://github.com/apvarun/blist-hugo-theme), thanks to the people behind it.

this project uses `uv` as python package manager.
for css, `tailwind` is used, the main file is `static/css/style.css` and the built version is `static/css/built.css`, do build before checking the page.


you should add a `.env` file containing:
1. `ALLOWED_HOSTS`, a comma separated list.
2. `POSTGRES_NAME`, database name.
3. `POSTGRES_PASSWORD`, database password.
4. `SECRET_KEY`, secret key string
5. `DJANGO_MODE`, either don't set it, or set as `prod`
6. `ADMIN_URL`, production setting, default to `admin/`
7. `DEBUG`, in production it defaults to `False`

INTERNAL_IPS is set to 127.0.0.1, change that if you are using docker
