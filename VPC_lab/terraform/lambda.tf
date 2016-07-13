# iam role

resource "aws_iam_role" "LambdaRole" {
  name = "LambdaRole"
  assume_role_policy = <<EOF
{
      "Version": "2012-10-17",
      "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
}
EOF
  path = "/"
  
}

# iam policy
resource "aws_iam_policy" "LambdaPolicy" {
  name = "LambdaPolicy"
  path = "/"
  description = "My test policy"
  policy = <<EOF
{
    "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*"
      }, {
        "Effect": "Allow",
        "Action": [
          "ec2:DescribeInstances"
        ],
        "Resource": "*"
      }
    ]
}
EOF
}

# iam policy attachment 

resource "aws_iam_policy_attachment" "test-attach" {
    name = "test-attachment"
    roles = ["${aws_iam_role.LambdaRole.name}"]
    policy_arn = "${aws_iam_policy.LambdaPolicy.arn}"
}

# lambda function

resource "aws_lambda_function" "test_lambda" {
    description = "This function will list instance IDs and their state."
    function_name = "DescribeInstancesLambda"
    role = "${aws_iam_role.LambdaRole.arn}"
    handler = "mylambda.lambda_handler"
    runtime =  "python2.7"
    s3_bucket =  "surefoot.${var.region}"
    s3_key = "lambda.zip"
    timeout = 120
}
