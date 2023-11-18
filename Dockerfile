# FROM pytorch/pytorch:latest
FROM python:3.8
# Set working directory
WORKDIR /opt

# Install dependencies
COPY . .
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8080

# Command to run the application
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
# CMD ["tail","-f","/dev/null"]
# CMD python run.py
# ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080","--reload"]
ENTRYPOINT ["python", "run.py"]