FROM python:3.11-bookworm

WORKDIR /reward-points
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Run server
EXPOSE 8080

ENTRYPOINT [ "python3" ]
CMD ["src/main.py"]