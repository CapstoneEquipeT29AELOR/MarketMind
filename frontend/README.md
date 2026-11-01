# Frontend

Status: **TODO — no frontend application is included.**

Build the market dashboard here. Add the frontend package manifest,
application entrypoint, and build configuration after choosing the framework.
The existing proposal mentions React / Next.js; this organization does not
install or select either one.

| Folder | Add here |
| --- | --- |
| [src/pages/](src/pages/README.md) | Dashboard and stock detail views |
| [src/components/](src/components/README.md) | Charts, news cards, selectors, reusable states |
| [src/services/](src/services/README.md) | Calls to your own backend API |
| [src/styles/](src/styles/README.md) | Shared visual styles |

Start with a dashboard using local fixture data, then connect its API client
to the backend. Keep AI/provider keys out of browser code.
