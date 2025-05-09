FROM python:3.11-slim

RUN addgroup --system arrguardian && adduser --system --ingroup arrguardian --uid 568 arrguardian
RUN mkdir -p /app/data && chown -R arrguardian:arrguardian /app/data
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
RUN chown -R arrguardian:arrguardian /app
USER arrguardian
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
