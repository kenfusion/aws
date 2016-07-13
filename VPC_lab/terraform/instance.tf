# Public Instance

resource "aws_instance" "public" {
    ami = "${lookup(var.amis, var.region)}"
    instance_type = "t2.micro"
    key_name = "aws"
    vpc_security_group_ids = ["${aws_security_group.PublicSG.id}"]
    subnet_id = "${aws_subnet.public.id}"
        
    tags {
      Name = "Public Instance"
      Terraform = "True"  
  }
}

# Public Instance

resource "aws_instance" "private" {
    ami = "${lookup(var.amis, var.region)}"
    instance_type = "t2.micro"
    key_name = "aws"
    vpc_security_group_ids = ["${aws_security_group.PrivateSG.id}"]
    subnet_id = "${aws_subnet.private.id}"
        
    tags {
      Name = "Private Instance"
      Terraform = "True"  
  }
}
