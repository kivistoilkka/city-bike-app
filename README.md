# Helsinki city bike app

My solution for Solita Dev Academy Finland 2023 pre-assignment.

Frontend is located in [separate repository](https://github.com/kivistoilkka/city-bike-app-frontend).

## Installation

Application is written and it is tested with Python 3.8 and it's dependencies are managed with [Poetry](https://python-poetry.org/). Pip and venv was used for Render deployment. PostgreSQL was installed using [installation script](https://github.com/hy-tsoha/local-pg).

1. Copy repository from GitHub

2. Install dependencies with command
```bash
poetry install
```

3. Create .env file and place it in the root of the project. Here is the example of my file used for development:
```bash
DATABASE_URL=postgresql+psycopg2:///city_bike_app_testing
TEST_DATABASE_URL=postgresql+psycopg2:///city_bike_app_testing
```

4. Download four CSV files linked in [assgnment repository](https://github.com/solita/dev-academy-2023-exercise), create directory 'data' in project root and place those files there.

5. Run program. It will build the database at the beginning of first run.

## Commands

Run backend
```bash
poetry run invoke start
```

Delete database tables and run backend with new build at the start
```bash
poetry run invoke start-with-build
```

Run backend in development mode with smaller dataset
```bash
poetry run invoke dev
```

Run tests
```bash
poetry run invoke test
```

Create test coverage report
```bash
poetry run invoke coverage-report
```

Build frontend and copy it to the backend folder (installed frontend has to be located in the sibling directory):
```bash
poetry run invoke build-frontend
```

More invoke commands can be found from tasks.py.

## Configuration

Configuration file is located [here](https://github.com/kivistoilkka/city-bike-app/blob/main/src/config/config.py).
