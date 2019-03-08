FROM ubuntu:bionic

RUN apt-get update

RUN apt-get install -y -f ca-certificates \
                    	 python3-all-dev \
                    	 python3-venv \
                       redis-server \
                    	 postgresql-server-dev-10 \
                       build-essential

RUN python3 -m venv /venv

ENV PATH="/venv/bin:$PATH"

# Set the working directory to /quiz
WORKDIR /quiz

# Copy the current directory contents into the container at /quiz
COPY . /quiz

RUN pip3 install -U pip wheel

RUN pip3 install incremental  # with requirements.txt wasn't installing

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
#CMD ["python3", "manage.py", "runserver"]

ENV PYTHONUNBUFFERED 1
