# json-lines-to-aws-sqs
read text file and send each line of it to aws sqs.

# requirements
- [python](https://www.python.org/downloads/)
- [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

## setup

### python

#### create environment
```shell
python3 -m venv env
```

#### activate environment
```shell
source env/bin/activate
```

#### install requirements
```shell
pip3 install -r requirements.txt
```

## local execution
```shell
python3 json-lines-to-aws-sqs.py "${file_path}" "${sqs_url}"
```

> change: 
> ${file_path} by the actuall file path to send
> ${sqs_url} by the actuall aws sqs url