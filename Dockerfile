FROM python:3.11
EXPOSE 6000
WORKDIR /app
RUN pip install flask

# Copy the current directory contents into the container at /app
COPY . /app
CMD ["flask", "run", "--host" , "0.0.0.0" ]
