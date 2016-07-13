# Network Access Control List
resource "aws_network_acl" "NetworkAcl" {
  vpc_id = "${aws_vpc.main.id}"
  subnet_ids = ["${aws_subnet.public.id}", "${aws_subnet.private.id}"]
  
}

resource "aws_network_acl_rule" "ACLrule1" {
  network_acl_id = "${aws_network_acl.NetworkAcl.id}"
  rule_number = 100
  egress = true
  protocol = "all"
  rule_action = "allow"
  cidr_block = "0.0.0.0/0"
}

resource "aws_network_acl_rule" "ACLrule2" {
  network_acl_id = "${aws_network_acl.NetworkAcl.id}"
  rule_number = 100
  egress = false
  protocol = "all"
  rule_action = "allow"
  cidr_block = "0.0.0.0/0"
}
