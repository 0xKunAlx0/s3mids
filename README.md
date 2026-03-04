# s3mids

s3mids is created to detect AWS S3 misconfigurations that many existing tools miss due to region-based bucket access behavior. Some buckets return “NoSuchBucket” when queried from the wrong endpoint but remain accessible. This tool identifies the correct region and tests for public access, upload, delete, and takeover risks.

<img width="957" height="240" alt="image" src="https://github.com/user-attachments/assets/f736980c-152e-47fb-8f4d-327ffbfca90a" />


It helps security researchers and bug bounty hunters identify:

* Publicly accessible buckets
* Anonymous upload permissions
* Public read access
* Bucket misconfigurations
* Possible S3 takeover vulnerabilities

---

## Features

* Detects whether an **S3 bucket exists**
* Automatically identifies the **correct AWS region**
* Checks for **public bucket listing**
* Tests **anonymous upload access**
* Verifies if uploaded objects are **publicly readable**
* Tests **anonymous delete permissions**
* Detects **possible S3 bucket takeover**
* Supports **single and multiple target scanning**

---

## Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/s3mids.git
```

Navigate to the project directory:

```
cd s3mids
```

Install Python dependencies:

```
pip install -r requirements.txt
```

---

## Requirements

* Python 3.x
* AWS CLI
* Python package:

  * requests

Install AWS CLI if it is not installed:

```
sudo apt install awscli
```

or

```
pip install awscli
```

---

## Usage

### Scan a Single Bucket

```
python3 s3mids.py -b bucket-name
```

Example:

```
python3 s3mids.py -b example-bucket
```

---

### Scan Multiple Targets

Provide a file containing bucket names or domains.

```
python3 s3mids.py -l buckets.txt
```

---

### Specify a Custom PoC File for Upload Testing

```
python3 s3mids.py -l buckets.txt -f poc.txt
```

---

## Example Output

```
[+] Bucket exists
[+] Region: ap-south-1

[*] Checking public listing...
[OK] No public listing access

[*] Testing anonymous upload...
[CRITICAL] Anonymous upload SUCCESS

[+] Uploaded to:
http://example-bucket.s3.amazonaws.com/poc-test.txt
```

---

## Example Bucket List File

```
example-bucket
cdn.example.com
assets.example.org
```
<img width="739" height="443" alt="image" src="https://github.com/user-attachments/assets/e744611f-5377-4cee-aaad-90e4a1071b53" />

---

## requirements.txt

```
requests>=2.31.0
```

---

## Disclaimer

This tool is intended for **security research and authorized testing only**.

Do **not** use this tool against systems without **proper permission**.
The author is **not responsible for misuse** of this tool.

---

## Author

Developed by **KunAl Dhumal [Linkedin](https://www.linkedin.com/in/kunal-dhumal-47356721a/)**

---

## License

This project is licensed under the **MIT License**.
