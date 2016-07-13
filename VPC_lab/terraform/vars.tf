variable "region" {
    default = "us-east-1"
}

variable "amis" {
    default = {
			ap-northeast-1 = "ami-cbf90ecb"
      ap-southeast-1 = "ami-68d8e93a"
      ap-southeast-2 = "ami-fd9cecc7"
			eu-central-1   = "ami-a8221fb5"
      eu-west-1      = "ami-a10897d6"
      sa-east-1      = "ami-b52890a8"
      us-east-1      = "ami-08111162"
      us-west-1      = "ami-d114f295"
      us-west-2      = "ami-e7527ed7"
    }
}

