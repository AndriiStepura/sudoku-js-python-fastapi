FROM python:3.14-slim

# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
# FROM python:3.14.0-alpine3.22

# ---- Copy app source ----
COPY . .
COPY /backend/requirements.txt /backend

# ---- Install dependencies
RUN pip install --no-cache-dir -r /backend/requirements.txt

# ---- Expose port ----
EXPOSE 8000

WORKDIR /backend
# ---- Run server ----
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# set path to our python api file
# ENV MODULE_NAME="main.app"
# copy contents of project into docker
# COPY ./ /app
# install poetry

# RUN pip install --no-cache-dir -r requirements.txt

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]