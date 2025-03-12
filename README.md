### **GitHub Repository Description for AWS Lambda Image Processing Project**  

---

### **Serverless Image Processing with AWS Lambda and S3**  
This project demonstrates how to build a **serverless image processing pipeline** using **AWS Lambda** and **Amazon S3**. Whenever an image is uploaded to an S3 bucket, a Lambda function automatically resizes it and stores the processed image in another S3 bucket.
---

### **🚀 Features**
✅ **Fully Serverless** – No infrastructure management required.  
✅ **Event-Driven** – Automatically processes images when uploaded to S3.  
✅ **Uses AWS Lambda Layers** – Includes **Pillow (PIL)** for image processing.  
✅ **Optimized for Scalability** – Processes images on-demand.  

---

### **🛠️ Tech Stack**
- **AWS Lambda** (Event-driven function execution)  
- **Amazon S3** (Storage for original and processed images)  
- **AWS Lambda Layers** (Includes Pillow for image processing)  
- **IAM Roles** (Permissions for Lambda to access S3)  
- **Amazon CloudWatch** (Logs for debugging and monitoring)  

---

### **📂 Project Structure**
```
📂 lambda-image-processing
│── 📂 package/                  # (Optional) Lambda deployment package
│── 📄 lambda_function.py        # Main Lambda function code
│── 📄 requirements.txt          # Dependencies for deployment
│── 📄 README.md                 # Project documentation
```

---

### **📝 Setup & Deployment**
#### **Clone this repository**
```sh
git clone https://github.com/EngMohamedKemany/awsImgResize.git
Source Bucket: s3://image-upds-bkt
Destination Bucket: s3://prcsd-img-bkt
```

---

### **📜 AWS Lambda Code (`lambda_function.py`)**
```python
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
```

---

### **🔧 AWS Lambda Configuration**
1. **Runtime**: Python 3.x  
2. **Memory**: 128 MB (Recommended: 256MB for faster processing)  
3. **Timeout**: 30 seconds  
4. **Handler**: `lambda_function.lambda_handler`  
5. **Layers**: Add a **public Pillow Layer** (See below)  

#### **🖼️ Adding Pillow (PIL) as a Layer**
1. **Find the ARN** for **Pillow** from [Klayers GitHub](https://github.com/keithrozario/Klayers).
2. **Attach the layer** to your Lambda function.

Example ARN for **us-east-1** (Python 3.8):
```
arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p312-pillow:2
```

---

### **🚀 How It Works**
1. A user uploads an image to **S3 (input bucket)**.
2. AWS **S3 triggers Lambda** when a new file is uploaded.
3. Lambda **resizes the image** using Pillow.
4. The processed image is **saved in the output S3 bucket**.

---

### **✅ Testing the Setup**
1. Upload an image manually via AWS **S3 Console**.
2. Check **CloudWatch Logs** for any errors.
3. Verify that the **resized image appears** in the output S3 bucket.

---

### **🔒 IAM Permissions**
Ensure that your **Lambda execution role** has the following permissions:

```json
{
    "Effect": "Allow",
    "Action": [
        "s3:GetObject",
        "s3:PutObject"
    ],
    "Resource": [
        "arn:aws:s3:::your-source-bucket/*",
        "arn:aws:s3:::processed-images-bucket/*"
    ]
}
```

---

### **📌 Future Enhancements**
- ✅ **Watermarking images** before saving  
- ✅ **Use DynamoDB** to store image metadata  
- ✅ **Expose an API Gateway** for uploads  
- ✅ **Support multiple image formats**  

---

### **📜 License**
This project is open-source under the **MIT License**.

---

### **💡 Contributing**
Feel free to submit **pull requests** or **issues** to improve this project! 🚀

---

Let me know if you need any modifications before publishing this! 🚀🔥
