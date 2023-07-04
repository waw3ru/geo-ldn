# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

### Docker deployment ###

```yaml
version: '3.8'

services:
  web:
    image: ghcr.io/zisake/geo-ldn/geo-ldn-site:latest
    pull_policy: always
    restart: on-failure
    ports:
      - 5050:8000
    env_file: .env # please check .env.example
```
