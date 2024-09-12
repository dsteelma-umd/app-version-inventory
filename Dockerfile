# Dockerfile for the generating app-version-inventory application Docker image
#
# To build:
#
# docker build -t app-version-inventory:<VERSION> -f Dockerfile .
#
# where <VERSION> is the Docker image version to create.
FROM python:3.12.6


# Create a user for the app.
RUN addgroup --gid 9999 app && \
    adduser --uid 9999 --gid 9999 --disabled-password --gecos "Application" app && \
    usermod -L app

USER app

# Make a subdirectory in the home directory for the application and make in the
# work directory
RUN mkdir /home/app/app-version-inventory

# Configure the main working directory. This is the base
# directory used in any further RUN, COPY, and ENTRYPOINT
# commands.
WORKDIR /home/app/app-version-inventory

# Add /home/app/.local/bin where the Python dependencies will be installed
# to the PATH
ENV PATH=/home/app/.local/bin:$PATH

# Copy the requirements.txt file holding the Python packages to install and
# run "pip install". This is a separate step so the dependencies will be cached
# unless changes to the file are made.
COPY --chown=app:app pyproject.toml /home/app/app-version-inventory

RUN cd /home/app/app-version-inventory && \
    pip install '.' && \
    cd ..

# Copy the main application
ENV PYTHONUNBUFFERED=1
COPY  --chown=app:app . /home/app/app-version-inventory

# Install the main application
RUN cd /home/app/app-version-inventory && \
    pip install .

