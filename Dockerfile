ARG BASE_IMAGE=python:3.12
FROM $BASE_IMAGE

# Set working directory to `/code`
WORKDIR /code

# Copy all files into `/code/app` (update `.dockerignore` to not include everything
COPY . /code/app

# Install project requirements
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

# Run tests in directory
CMD ["pytest", "app/tests/"]
