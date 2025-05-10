FROM python:3.11-slim

RUN addgroup --system gaardian && adduser --system --ingroup gaardian --uid 568 gaardian
RUN mkdir -p /app/data && chown -R gaardian:gaardian /app/data
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
RUN chown -R gaardian:gaardian /app
USER gaardian
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
