import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get bucket name and file key from S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    print(f"Event: {event}")
    print(f"Bucket: {bucket_name}")
    print(f"Object Key: {object_key.replace(".jpg", "")}")
    
    
    # Define output bucket
    output_bucket = 'prcsd-img-bkt'
    
    # Download image from S3
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    image = Image.open(response['Body'])
    
    # Resize image
    image = image.resize((300, 300))
    
    # Convert image to bytes
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    
    # Upload resized image to output bucket
    key1 = f"resized-{object_key.replace(".JPG", "")}" + ".jpeg"
    s3.put_object(Bucket=output_bucket, Key= key1, Body=buffer, ContentType="image/jpeg")
    
    return {
        'statusCode': 200,
        'body': f"Image {object_key} processed and saved as resized-{object_key}."
    }
