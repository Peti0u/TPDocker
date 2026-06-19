# [Dynamic Django](https://dynamic-django.onrender.com/)

**Dynamic Programming Patterns** applied in `Python/Django` - actively supported by `AppSeed`. 

> LIVE DEMOs & [official documentation](https://app-generator.dev/docs/developer-tools/dynamic-django/index.html)

- Dynamic DataTables: https://dynamic-django.onrender.com/dynamic-dt/sales/
- Dynamic Charts: https://dynamic-django.onrender.com/dynamic-charts/sales/
  - `PIE`: [DEMO](https://dynamic-django.onrender.com/dynamic-charts/sales/?chart_id=2), [EMBED](https://dynamic-django.onrender.com/dynamic-charts/embed/2/)
  - `POLAR`: [DEMO](https://dynamic-django.onrender.com/dynamic-charts/sales/?chart_id=10), [EMBED](https://dynamic-django.onrender.com/dynamic-charts/embed/10/)
  - `DONUT`: [DEMO](https://dynamic-django.onrender.com/dynamic-charts/sales/?chart_id=8), [EMBED](https://dynamic-django.onrender.com/dynamic-charts/embed/8/)

## Features 

- [OK] Dynamic DT
- [OK] Dynamic Charts
- [OK] Dynamic API via DRF
- [OK] Powerful `CLI` tools      

## Quick Start

> NOTE: Requires a [purchase](https://appseed.gumroad.com/l/devtool-dynamic-django), secured by GUMROAD.
 
```
# Clone Repo
$ git clone https://github.com/app-generator/priv-dynamic-django.git
```

> Create VENV

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

> Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

> Start the Project

```bash
$ python manage.py createsuperuser # create the admin
$ python manage.py runserver       # start the project
```

## Update model 

```bash
$ python
>>> from cli import *
>>> add_model('home', 'Stats')
>>> # Syntax: model_add_field('APP_NAME_HERE', 'MODEL_NAME_HERE', 'FIELD_NAME',  'FIELD_TYPE') 
>>> add_model_field('home', 'Stats', 'aInt',  'int') 
>>> add_model_field('home', 'Stats', 'aChar', 'str')
>>> add_model_field('home', 'Stats', 'aText', 'text')
```

The file is automatically reformated using `black` and DB migrated.

## DB Backup / RESET / Restore

```bash
$ python manage.py dbbackup  -o 20240930-001.dump  # backup 
$ python manage.py reset_db                        # RESET_DB [ Danger, all tables wipped ]
$ python manage.py dbrestore -i 20240930-001.dump  # restore 
```

---
[Dynamic Django](https://dynamic-django.onrender.com/) - actively supported by `AppSeed`.
