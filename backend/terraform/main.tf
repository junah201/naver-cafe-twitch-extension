module "lambda_default_role" {
  source = "./modules/role"
  name   = "LambdaDefault"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt"
      ],
      "Resource": "arn:aws:kms:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:*"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

// s3
resource "aws_s3_bucket" "lambda_build_bucket" {
  bucket = var.lambda_build_bucket
}

// layer
module "request_layer" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "request_layer"
  description         = "request_layer"
  compatible_runtimes = ["python3.10"]

  source_path = "../layers/request_layer"

  store_on_s3 = true
  s3_bucket   = aws_s3_bucket.lambda_build_bucket.id
}

// lambda
module "get_root_lambda" {
  depends_on = [aws_s3_bucket.lambda_build_bucket]

  source = "terraform-aws-modules/lambda/aws"

  function_name = "get_root"
  description   = "GET /"
  handler       = "main.lambda_handler"
  runtime       = "python3.10"
  timeout       = 120
  source_path   = "../lambdas/get_root"

  # store_on_s3 = true
  s3_bucket   = var.lambda_build_bucket

  create_role = false
  lambda_role = module.lambda_default_role.role_arn

  layers = [
    module.request_layer.lambda_layer_arn
  ]

  tags = {
    version = "v1"
  }
}

module "get_config" {
  depends_on = [aws_s3_bucket.lambda_build_bucket]

  source = "terraform-aws-modules/lambda/aws"

  function_name = "get_config"
  description   = "GET /{id}/config"
  handler       = "main.lambda_handler"
  runtime       = "python3.10"
  timeout       = 120
  source_path   = "../lambdas/get_config"

  store_on_s3 = true
  s3_bucket   = var.lambda_build_bucket

  create_role = false
  lambda_role = module.lambda_default_role.role_arn

  layers = [
    module.request_layer.lambda_layer_arn
  ]

  tags = {
    version = "v1"
  }
}

module "post_config" {
  depends_on = [aws_s3_bucket.lambda_build_bucket]

  source = "terraform-aws-modules/lambda/aws"

  function_name = "post_config"
  description   = "POST /{id}/config"
  handler       = "main.lambda_handler"
  runtime       = "python3.10"
  timeout       = 120
  source_path   = "../lambdas/post_config"

  store_on_s3 = true
  s3_bucket   = var.lambda_build_bucket

  create_role = false
  lambda_role = module.lambda_default_role.role_arn

  layers = [
    module.request_layer.lambda_layer_arn
  ]

  tags = {
    version = "v1"
  }
}

module "get_posts" {
  depends_on = [aws_s3_bucket.lambda_build_bucket]

  source = "terraform-aws-modules/lambda/aws"

  function_name = "get_posts"
  description   = "POST /{id}/posts"
  handler       = "main.lambda_handler"
  runtime       = "python3.10"
  timeout       = 120
  source_path   = "../lambdas/get_posts"

  store_on_s3 = true
  s3_bucket   = var.lambda_build_bucket

  create_role = false
  lambda_role = module.lambda_default_role.role_arn

  layers = [
    module.request_layer.lambda_layer_arn
  ]

  tags = {
    version = "v1"
  }
}

module "get_boards" {
  depends_on = [aws_s3_bucket.lambda_build_bucket]

  source = "terraform-aws-modules/lambda/aws"

  function_name = "get_boards"
  description   = "POST /{id}/boards"
  handler       = "main.lambda_handler"
  runtime       = "python3.10"
  timeout       = 120
  source_path   = "../lambdas/get_boards"

  store_on_s3 = true
  s3_bucket   = var.lambda_build_bucket

  create_role = false
  lambda_role = module.lambda_default_role.role_arn

  layers = [
    module.request_layer.lambda_layer_arn
  ]

  tags = {
    version = "v1"
  }
}
