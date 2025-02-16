# Automated File Processing Pipeline Using AWS and Snowflake

##  Project Overview  
This project implements a **fully automated, serverless data engineering pipeline** that processes User Uploaded Files, transforms them, and loads them into **Snowflake** for real-time analytics. The pipeline leverages **AWS SFTP (Transfer Family), S3, Lambda, Glue, Snowpipe, and SQS**, ensuring a **cost-efficient, scalable, and event-driven** data flow.

## Architecture Diagram  
![High Level Architecture](https://github.com/saurabhchavan7/Automated-File-Processing-Pipeline-Using-AWS-and-Snowflake/blob/master/architecture/aws%20serverless.drawio.svg)

---

## Key Features  

**Automated Data Ingestion:** users upload ZIP files via AWS SFTP (Transfer Family), which are stored in **Amazon S3 (Landing Zone)**.  
**Serverless Processing:** AWS Lambda unzips files, processes CSV data, and triggers AWS Glue for further transformation.  
**Optimized Data Storage:** AWS Glue converts CSV files into **Parquet format** (reducing storage and improving query performance).  
**Real-Time Data Loading:** **Snowpipe** continuously ingests Parquet files into **Snowflake** as soon as they arrive.  
**Event-Driven Processing:** AWS S3 event notifications and Amazon SQS automate workflow triggers, ensuring **near real-time** data ingestion.  
**Scalable & Cost-Effective:** The pipeline is **serverless**, reducing operational costs while scaling efficiently.

---

## Tools and Technologies Used  

| **Component**    | **Technology Used**               |
|-----------------|----------------------------------|
| **Data Ingestion** | AWS SFTP (Transfer Family), S3 |
| **Processing**  | AWS Lambda, AWS Glue, PySpark   |
| **Storage**     | S3 (Landing, Curated, Published Layers) |
| **Data Warehouse** | Snowflake (Table & Schema Management) |
| **Automation**  | AWS Lambda, Glue, Snowpipe, S3 Events, SQS |
| **File Formats** | CSV → Parquet Conversion |
| **Security**    | IAM Roles, Least Privilege Access, SSH Authentication |

---

## Project Steps  

### Step 1: Setting Up Amazon S3 Bucket  
- Created an **S3 bucket** with three layers:
  - **Landing Zone:** Stores raw ZIP files from users.
  - **Curated Zone:** Stores extracted CSV files after processing.
  - **Published Zone:** Stores transformed Parquet files for Snowflake ingestion.

### Step 2: Configuring AWS Transfer Family (SFTP) for user File Upload  
- Deployed an **AWS Transfer Family SFTP server** as the entry point for user files.  
- Configured **IAM roles** for least-privilege access.  
- Assigned SSH key-based authentication for secure vendor access.  

### Step 3: Automating Unzipping & Processing with AWS Lambda  
- Set up an **S3 Event Trigger** to invoke **AWS Lambda** upon ZIP file arrival in the **Landing Zone**.  
- Lambda function:
  - **Downloads ZIP files** from S3.
  - **Extracts CSV files** and moves them to the **Curated Zone**.
  - **Triggers AWS Glue** to start the data transformation process.

### Step 4: Transforming Data with AWS Glue  
- AWS Glue reads **Curated Zone CSV files** and converts them into **Parquet format**.  
- Transformed files are stored in the **Published Zone**.  
- **Benefits of Parquet**:
  - Columnar storage for **faster queries**.
  - **Compression techniques** reduce storage costs.

### Step 5: Real-Time Data Loading with Snowflake & Snowpipe  
- **Configured an External Stage** in Snowflake pointing to the **Published Zone** in S3.  
- **Created a Snowpipe** that:
  - Listens to **S3 Event Notifications** (via Amazon SQS).
  - **Automatically executes COPY INTO** to load new Parquet files into Snowflake tables.

---

##  Architecture Flow  

1️. **Users upload ZIP files** to the SFTP server (AWS Transfer Family).  
2️. *AWS S3 (Landing Zone)** stores the uploaded ZIP files.  
3️. **AWS Lambda gets triggered** via S3 event notification:
   - Unzips files.
   - Extracts CSV files.
   - Moves them to the Curated Layer.
   - Triggers AWS Glue for transformation.  
4️. **AWS Glue** converts CSV files into **Parquet format** and saves them in the **Published Layer**.  
5️. **Amazon SQS receives notifications** whenever new Parquet files arrive.  
6️. **Snowpipe listens to SQS and auto-ingests** Parquet data into Snowflake.  
7️. **Data is ready for querying in Snowflake** for analytics and business intelligence.  

---

##  Security Measures  

**IAM Role-Based Access** – Enforced least privilege access across AWS services.  
**SFTP Authentication** – Used **public-private key pairs** for user access.  
**Encrypted Data Transfer** – Ensured secure file uploads to AWS Transfer Family.  
**Restricted Bucket Access** – Only specific services (Lambda, Glue, Snowpipe) can interact with S3.  

---

## Business Impact  

**Real-time Data Availability** – Users' files are processed and ingested **within minutes**.  
**Reduced Storage Costs** – Parquet format **minimized storage** requirements.  
**Faster Queries** – Snowflake’s columnar storage enabled **50% faster analytics**.  
**Serverless & Scalable** – No manual intervention required; pipeline scales automatically.  

---


