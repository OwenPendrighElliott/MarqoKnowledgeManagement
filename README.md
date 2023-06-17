# Marqo Knowledge Management

This project is a small demo of a knowledge management system that integrates Marqo and ChatGPT. You can spin this demo up easily on a laptop.

![Demo](readme_assets/Marqo%20ChatGPT%20Organisational%20Knowledge%20Demo.mov)

## Project Structure

### `frontend/`

This folder contains the code for the frontend of the application, the frontend is written with NextJS and TypeScript.

### `backend/`

This folder contains the backend code, the backend is written as a webserver using flask.

## Running for development

### Frontend

```
cd frontend
npm i
npm run dev
```

### Backend

```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m flask run --debug
```

### Marqo

[Follow the getting started guide to run the docker image.](https://docs.marqo.ai/0.0.17/)


## Formatting code

### Frontend

```
cd frontend
npm run format
```

### Backend

```
cd backend
black .
```
