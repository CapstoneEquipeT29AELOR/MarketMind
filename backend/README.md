# Backend

Status: **TODO — no API server is included.**

Add Python application code here. Choose a web framework, define package
imports/entrypoints, and record dependencies in requirements/backend.txt
when that code is introduced. That dependency file does not exist yet.

| Folder | Responsibility |
| --- | --- |
| [api/](api/README.md) | HTTP routes, request/response validation, app startup |
| [services/](services/README.md) | Application workflows and data freshness |
| [integrations/](integrations/README.md) | External financial, news, and AI providers |
| [database/](database/README.md) | Connections, schema, queries, migrations |

Start with a health endpoint and one price/news response backed by controlled
fixtures, then integrate the database and providers. ML research code remains
under ../ml/; do not start a training run for every dashboard request.
