
# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  instance_tenancy = "default"
  enable_dns_support = true
  enable_dns_hostnames = true
 
  tags {
    Name = "TerraformVPC"
    Terraform = "True"        
  }
}

#IGW 
resource "aws_internet_gateway" "main" {
  vpc_id = "${aws_vpc.main.id}"
  
  tags {
    Name = "MyIGW"
    Terraform = "True"        
  }
}

#Private Subnet

resource "aws_subnet" "private" {
  cidr_block = "10.0.0.0/24"
  map_public_ip_on_launch = false
  vpc_id = "${aws_vpc.main.id}"
  availability_zone = "us-east-1a"

  tags {
    Name = "Private Subnet"
    Terraform = "True"  
  }
}


# Public Subnet
resource "aws_subnet" "public" {
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true
  vpc_id = "${aws_vpc.main.id}"
  availability_zone = "us-east-1a"

  tags {
    Name = "Public Subnet"
    Terraform = "True"  
  }
}

# DHCP Options and association

resource "aws_vpc_dhcp_options" "DHCPOptions" {
  domain_name = "ec2.internal"
  domain_name_servers = ["AmazonProvidedDNS"]
  tags {
    Name = "DCHP Options Set"
    Terraform = "True"  
  }
}
resource "aws_vpc_dhcp_options_association" "VPCDHCPOptionsAssociation" {
  vpc_id = "${aws_vpc.main.id}"
  dhcp_options_id = "${aws_vpc_dhcp_options.DHCPOptions.id}"
}

# EIP

resource "aws_eip" "nat" {
  vpc      = true
}

# NAT

resource "aws_nat_gateway" "nat" {
    allocation_id = "${aws_eip.nat.id}"
    subnet_id = "${aws_subnet.public.id}"
}
