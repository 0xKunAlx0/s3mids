# S3MIDS

**S3MIDS** is a lightweight tool designed to detect common **AWS S3 bucket misconfigurations** and **potential bucket takeover scenarios**.

It helps security researchers and bug bounty hunters quickly identify:
- Publicly accessible buckets
- Anonymous upload permissions
- Public read access
- Misconfigured buckets
- Potential S3 takeover vulnerabilities

---

## Features

- Detects whether an **S3 bucket exists**
- Automatically identifies the **correct AWS region**
- Checks for **public bucket listing**
- Tests **anonymous upload access**
- Verifies if uploaded objects are **publicly readable**
- Tests **anonymous delete permissions**
- Detects **possible S3 bucket takeover**
- Supports **single and multiple target scanning**

---

## Installation


Clone the repository:

`git clone https://github.com/YOUR_USERNAME/s3mids.git`

Navigate into the project directory:

`cd s3mids`

Install dependencies:

`pip install -r requirements.txt`
