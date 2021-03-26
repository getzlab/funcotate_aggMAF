FROM gcr.io/broad-getzlab-workflows/snvmerger:v14

WORKDIR build
# build steps go here
# remember to clear the build directory!

WORKDIR /app
ENV PATH=$PATH:/app
COPY src/* ./
