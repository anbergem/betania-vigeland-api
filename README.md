# Betania Vigeland API
A simple API that serves some utility functions for use in Betania Vigeland.

## Installation
Download [poetry](https://python-poetry.org).
```shell
poetry install
```

## Integrations
The api is hosted on ***todo***.

- `/planning-center`<br/>
  Planning Center integrations require all requests to be sent with a 
  basic http auth token, username and password. These are forwarded to
  the Planning Center API.They can be found on [Planning Center's Development
  Page](https://developer.planning.center/docs/#/overview/).
  - `/get-confirmed-team-members`<br/>
Gets the confirmed team members for the upcoming sunday's service.