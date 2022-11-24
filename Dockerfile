# Step 1 - linting code
FROM eeacms/pylint:latest as linting
WORKDIR /code
COPY ["./Code/*.py","./"]
RUN /docker-entrypoint.sh pylint --disable=all --exit-zero

# Step 2 - running after linting
FROM python:3.6-alpine as server
WORKDIR /app
# Copy all packages instead of rerunning pip install
COPY ["./Code","./"]
ENV aws_access_key_id="someid"
ENV aws_secret_access_key="somesecret"
ENV region="eu-west-1"
ENV interval="100"
RUN pip install -r requirements.txt
CMD ["python", "run_app.py"]
