# Hagstófa Íslands ETL Pipeline

Einfalt ETL pipeline sem sækir gögn frá hagstöfu íslands api, hreinsar þau og vistar á aws s3.

## Hvað gerir þetta?

1. **Extract**: Sækir gögn um upplýsingatæknifyrirtæki frá api
2. **Transform**: Hreinsar og formaterar gögnin með pandas
3. **Load**: Vistar CSV skrá og plot í s3

## Tech stack

- Python
- AWS Lambda
- pandas, matplotlib, requests
- S3 fyrir storage

## Files

- `lambda_function.py` - Main Lambda handler
- `clean.py` - Data cleaning functions
- `requirements.txt` - Python dependencies


## Output

Lambda function vistar tvær skrár á S3:

- `data/upplysingataekni_YYYY-MM.csv` - Hrá gögn í CSV
- `plots/rekstrartekjur_trend_YYYY-MM.png` - Plot af rekstrartekjum

## Hvað lærði eg


- Lambda filesystem er read only nema `/tmp/`, þess vegna notum við BytesIO fyrir plots
