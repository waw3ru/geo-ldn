# GEO-LDN #

### Docker deployment ###

```yaml
version: '3.8'

services:
  web:
    image: ghcr.io/<OWNER>/geo-ldn/geo-ldn-site:latest
    pull_policy: always
    restart: on-failure
    ports:
      - 5050:8000
    env_file: .env # please check .env.example
```
