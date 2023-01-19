# Wedding

Source code for wedding website for Anna and Clark's double wedding.
Built with django and deployed on fly.io.

## Project Structure

* `/api/` Folder contains the base Django API, settings, urls, etc.
* `/guests/` Folder contains the wedding website source code.
* `/ping/` Folder contains a health check endpoint.
* `/templates/` Folder contains the wedding website and email HTML.

## Run locally

To run locally one must have Docker installed. From the root directory of the project use docker compose to deploy a local version of the wedding website and postgres database:

```bash
docker compose up
```

There are a number of environment variables that are not included in the repo and should be edited locally (if needed). Ddd the following to `/.envs/.local/.django` and change as needed:

```bash
DEBUG=1
SECRET_KEY=fake_key
USE_DOCKER=yes
IPYTHONDIR=/app/.ipython
DJANGO_SUPERUSER_PASSWORD=FAKE_PASS
DJANGO_SUPERUSER_EMAIL=FAKE_SUPER_EMAIL
DJANGO_SUPERUSER_USERNAME=FAKE_USER
SENDGRID_API_KEY=FAKE_SENDGRID_KEY
```

## Deploy

To deploy, install [flyctl](https://fly.io) and run:

```bash
flyctl deploy
```
