# Terraform Notes

**DoKyu**  
2023년 12월 17일 시작  
최종 정리: 2026년 기준 (Obsidian용)

---

## 1. 개인 프로젝트 개요 (PDF Page 1~2)

### Terraform usage and AWS + Gitlab

- AWS S3 access is required
- Src: reading from S3 and send it to SQS // by tf
- Dst: queue url is SQS URL
- Processor consume SQS streaming and write on SNF T

Gitlab versioning and usage  
→ Gitlab CI/CD + Terraform으로 S3 → SQS → Processor → SNF T 파이프라인 구축 목표

---

## 2. 기본 구조 및 모듈 아이디어 (Page 3~5)

### 추천 프로젝트 구조 예시
```text
project/
├── main.tf
├── variables.tf
├── terraform.tfvars
├── modules/
│   ├── s3/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── sqs/
│   └── executor/
└── .gitlab-ci.yml
```

### S3 Bucket Policy JSON 예시 (Page 4~5)

```json
{
  "Version": "2012-10-17",
  "Id": "PolicyForConfigBucket",
  "Statement": [
    {
      "Sid": "AllowReadWrite",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ACCOUNT:role/executor-role"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::dev-config-executor/*"
    }
  ]
}
```
## 3. KodeKloud Basics 요약 (Page 6~19)

### IaC 비교 (Ansible vs Terraform)
- Ansible 예시
```yaml
 amazon.aws.ec2:
    key_name: mykey
    instance_type: t2.micro
    image: ami-123456
    wait: yes
    group: webserver
    count: 3
    vpc_subnet_id: subnet-29e63245
    assign_public_ip: yes

```
- Terraform 예시
```terraform
resource "aws_instance" "webserver" {
  ami           = "ami-0edab43b6fa892279"
  instance_type = "t2.micro"
}
``` 

- 선언형 기본 예시
```terraform
resource "aws_instance" "webserver" {
  ami           = "ami-0c2f25c1f66a1ff4d"
  instance_type = "t2.micro"
}

resource "aws_s3_bucket" "finance" {
  bucket = "finance-21092020"
  tags = {
    Description = "Finance and Payroll"
  }
}

resource "aws_iam_user" "admin-user" {
  name = "lucy"
  tags = {
    Description = "Team Leader"
  }
}
```
## 4. HCL 기본 실습 (Page 20~28)
- 가장 기본 local_file
```terraform
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```
- random_pet + local_file 조합 예시
```terraform
resource "random_pet" "server" {}

resource "local_file" "pet-name" {
  filename = "/root/${random_pet.server.id}.txt"
  content  = "My pet is ${random_pet.server.id}"
}
```
## 5. Variables & tfvars (Page 34~40)
- Map 변수 사용 예
```terraform
variable "file-content" {
  type = map(string)
  default = {
    "statement1" = "We love pets!"
    "statement2" = "We love animals!"
  }
}

resource "local_file" "my-pet" {
  filename = "/root/pets.txt"
  content  = var.file-content["statement1"]
}
```
#### 변수 우선순위 (Precedence)

1. -var 플래그
2. *.auto.tfvars
3. terraform.tfvars
4. TF_VAR_xxx
5. variables.tf default

## 6. Lifecycle 메타 인자 (Page 47~51)
- create_before_destroy
```terraform
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"

  lifecycle {
    create_before_destroy = true
    ignore_changes = [tags]
    prevent_destroy = true
    }
}

```
## 7. count & for_each (Page 57~59)
- count 예시
```terraform
variable "filenames" {
  default = ["/root/dogs.txt", "/root/cats.txt"]
}

resource "local_file" "pet" {
  count    = length(var.filenames)
  filename = var.filenames[count.index]
}
```
## 8. AWS IAM 실습 (Page 71~90)
- IAM User + Policy + Attachment (heredoc)
```terraform
resource "aws_iam_user" "admin" {
  name = "terraform-admin"
}

resource "aws_iam_policy" "admin-policy" {
  name        = "AdminFullAccess"
  path        = "/"
  description = "Full admin access"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_user_policy_attachment" "attach" {
  user       = aws_iam_user.admin.name
  policy_arn = aws_iam_policy.admin-policy.arn
}
```
## 9. S3 Bucket & Object (Page 91~96)
```terraform
resource "aws_s3_bucket" "config" {
  bucket = "dev-config-executor"
  tags = {
    Name        = "ConfigBucket"
    Environment = "dev"
  }
}

resource "aws_s3_object" "config-file" {
  bucket = aws_s3_bucket.config.id
  key    = "config.json"
  source = "files/config.json"
}
```
## 10. DynamoDB 예시 (Page 98~102)
```terraform
resource "aws_dynamodb_table" "cars" {
  name         = "cars"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "VIN"

  attribute {
    name = "VIN"
    type = "S"
  }
}

resource "aws_dynamodb_table_item" "car1" {
  table_name = aws_dynamodb_table.cars.name
  hash_key   = aws_dynamodb_table.cars.hash_key

  item = <<EOF
{
  "VIN": {"S": "1HGCM82633A004352"},
  "Make": {"S": "Honda"},
  "Model": {"S": "Accord"},
  "Year": {"N": "2003"}
}
EOF
}
```
## 11. Remote Backend + State Locking (Page 103~110)
```terraform
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```
## 12. EC2 + User Data + Provisioner (Page 114~145)
- EC2 + User Data + remote-exec
```terraform
resource "aws_instance" "web" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.mykey.key_name
  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install nginx -y
              systemctl start nginx
              systemctl enable nginx
              EOF

  provisioner "remote-exec" {
    inline = [
      "sudo systemctl status nginx"
    ]

    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = file("~/.ssh/mykey.pem")
      host        = self.public_ip
    }
  }
}
```
## 13. Modules 예시 (Page 156~170)
- 모듈 디렉토리 구조
```text
modules/
└── webserver/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```
- 모듈 호출 (root)
```hcl
module "web" {
  source        = "./modules/webserver"
  instance_type = "t3.micro"
  ami           = "ami-0c55b159cbfafe1f0"
  key_name      = "mykey"
}
```