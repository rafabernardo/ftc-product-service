resource "aws_security_group" "sg" {
  name   = var.security_group_name
  vpc_id = var.vpc_id
}

resource "aws_security_group_rule" "sg_ingress" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.sg.id
}

resource "aws_security_group_rule" "sg_ingress_vpc" {
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["172.31.0.0/16"]
  security_group_id = aws_security_group.sg.id
}

resource "aws_security_group_rule" "sg_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.sg.id
}
