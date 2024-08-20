.. _installation_environment_config:

===================================
Environment configuration reference
===================================

The Objects and Objecttypes APIs can be run both as a Docker container or a VPS / dedicated server. It relies on other services, such as
database and cache backends, which can be configured through environment
variables.

Available environment variables
===============================

Required settings
-----------------

* ``DJANGO_SETTINGS_MODULE``: which environment settings to use. Available options:

  - ``objects.conf.docker`` or ``objecttypes.conf.docker``
  - ``objects.conf.dev`` or ``objecttypes.conf.dev``
  - ``objects.conf.ci`` or ``objecttypes.conf.ci``

* ``SECRET_KEY``: secret key that's used for certain cryptographic utilities. You
  should generate one via
  `miniwebtool <https://www.miniwebtool.com/django-secret-key-generator/>`_

* ``ALLOWED_HOSTS``: A comma separated (without spaces!) list of domains that
  serve the installation. Used to protect against ``Host`` header attacks.
  Defaults to ``*`` for the ``docker`` environment and defaults to
  ``127.0.0.1,localhost`` for the ``dev`` environment.

* ``CACHE_DEFAULT``: A Redis cache driver is required. Defaults to ``redis:6379/0``.

Common settings
---------------

* ``DB_HOST``: Hostname of the PostgreSQL database. Defaults to ``db`` for the
  ``docker`` environment, otherwise defaults to ``localhost``.

* ``DB_USER``: Username of the database user. Defaults to ``objects`` or ``objecttypes``,

* ``DB_PASSWORD``: Password of the database user. Defaults to ``objects`` or ``objecttypes``,

* ``DB_NAME``: Name of the PostgreSQL database. Defaults to ``objects`` or ``objecttypes``,

* ``DB_PORT``: Port number of the database. Defaults to ``5432``.

* ``CELERY_BROKER_URL``: URL for the Redis task broker for Celery. Defaults
  to ``redis://127.0.0.1:6379/1``.

* ``CELERY_RESULT_BACKEND``: URL for the Redis result broker for Celery.
  Defaults to ``redis://127.0.0.1:6379/1``.

Elastic APM settings
--------------------

An integration with `Elastic APM <https://www.elastic.co/observability/application-performance-monitoring>`_
can be configured by setting the following environment variables

* ``ELASTIC_APM_SERVICE_NAME``: the name of the service in APM, i.e. "Objects API - staging"

* ``ELASTIC_APM_SERVER_URL``: the URL of the APM instance to connect with

* ``ELASTIC_APM_SECRET_TOKEN``: the token that is required to communicate with the APM instance

Other settings
--------------
* ``ENVIRONMENT``: An identifier for the environment, displayed in the admin depending on
  the settings module used and included in the error monitoring (see ``SENTRY_DSN``).
  The default is set according to ``DJANGO_SETTINGS_MODULE``. Good examples values are:

  * ``production``
  * ``test``

* ``SITE_ID``: The database ID of the site object. Defaults to ``1``.

* ``DEBUG``: Used for more traceback information on development environment.
  Various other security settings are derived from this setting! Defaults to
  ``True`` for the ``dev`` environment, otherwise defaults to ``False``.

* ``IS_HTTPS``: Used to construct absolute URLs and controls a variety of
  security settings. Defaults to the inverse of ``DEBUG``.

* ``SUBPATH``: If hosted on a subpath, provide the value here. If you provide
  ``/gateway``, the component assumes its running at the base URL:
  ``https://somedomain/gateway/``. Defaults to an empty string.

* ``SENTRY_DSN``: URL of the sentry project to send error reports to. Defaults
  to an empty string (ie. no monitoring).

* ``NOTIFICATIONS_DISABLED``: indicates whether or not notifications should be
  sent to the Notificaties API for operations on the Object endpoint.
  Defaults to ``True`` for the ``dev`` environment, otherwise defaults to ``False``.

* ``USE_X_FORWARDED_HOST``: whether to grab the domain/host from the ``X-Forwarded-Host``
  header or not. This header is typically set by reverse proxies (such as nginx,
  traefik, Apache...). Default ``False`` - this is a header that can be spoofed and you
  need to ensure you control it before enabling this.

* ``DISABLE_2FA``: whether to disable two-factor authentication. Defaults to ``False``.
  If set to ``False``, 2FA will be required if not using OIDC.

* ``LOG_REQUESTS``: whether to enable logging of outgoing HTTP requests. Defaults to ``False``.

* ``LOG_OUTGOING_REQUESTS_DB_SAVE``: whether to save logged requests to the database. Defaults to ``False``.

Initial superuser creation
--------------------------

A clean installation of Objects API comes without pre-installed or pre-configured admin
user by default.

Users of Objects API can opt-in to provision an initial superuser via environment
variables. The user will only be created if it doesn't exist yet.

* ``OBJECTS_SUPERUSER_USERNAME``: specify the username of the superuser to create. Setting
  this to a non-empty value will enable the creation of the superuser. Default empty.
* ``OBJECTS_SUPERUSER_EMAIL``: specify the e-mail address to configure for the superuser.
  Defaults to `admin@admin.org`. Only has an effect if ``OBJECTS_SUPERUSER_USERNAME`` is set.
* ``OBJECTS_SUPERUSER_PASSWORD``: specify the password for the superuser. Default empty,
  which means the superuser will be created _without_ password. Only has an effect
  if ``OBJECTS_SUPERUSER_USERNAME`` is set.

Initial configuration
---------------------

Both Objects API and Objecttypes API support `setup_configuration` management command,
which allows configuration via environment variables.
All these environment variables are described at :ref:`command line <installation_config_cli>`.


Specifying the environment variables
=====================================

There are two strategies to specify the environment variables:

* provide them in a ``.env`` file
* start the component processes (with uwsgi/gunicorn/celery) in a process
  manager that defines the environment variables

Providing a .env file
---------------------

This is the most simple setup and easiest to debug. The ``.env`` file must be
at the root of the project - i.e. on the same level as the ``src`` directory (
NOT *in* the ``src`` directory).

The syntax is key-value:

.. code::

   SOME_VAR=some_value
   OTHER_VAR="quoted_value"


Provide the envvars via the process manager
-------------------------------------------

If you use a process manager (such as supervisor/systemd), use their techniques
to define the envvars. The component will pick them up out of the box.
