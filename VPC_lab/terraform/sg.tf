# Public Security Group

resource "aws_security_group" "PublicSG" {
  name = "PublicSG"
  description = "Security Group for Public Subnet"
  vpc_id = "${aws_vpc.main.id}"
  
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  
  tags {
    Name = "Public Security Group"
    Terraform = "True"  
  }
}


# Private Security Group

resource "aws_security_group" "PrivateSG" {
  name = "PrivateSG"
  description = "Security Group for Public Subnet"
  vpc_id = "${aws_vpc.main.id}"
  
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
}
  
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    security_groups = ["${aws_security_group.PublicSG.id}"]
  }
  
 tags {
    Name = "Private Security Group"
    Terraform = "True"  
  }
}


