# FaunaMap Web Interface

This web interface offers interactive maps for exploring wildlife observations. The web interface is based on [https://github.com/HansSchouten/Laravel-Vue-Quasar-SPA](https://github.com/HansSchouten/Laravel-Vue-Quasar-SPA), leveraging Laravel, Vue.js and the [Quasar Framework](https://v1.quasar-framework.org/).

## Technical Features

- Laravel 5.7 
- Vue + VueRouter + Vuex + VueI18n + ESlint
- Authentication with JWT
- Socialite integration
- Quasar 1.0.0 Beta 11

## Installation

- `cp .env.example .env`
- Edit `.env` and set your database connection details
- `composer install`
- `php artisan key:generate`
- `php artisan jwt:secret`
- `php artisan migrate`
- `npm install` / `yarn`

## Usage

An account can be created via `/register`. After logging in via `/login` the dashboard is accessible.

### Development

```bash
# build and watch
npm run watch

# serve with hot reloading
npm run hot
```

### Production

```bash
npm run production
```
