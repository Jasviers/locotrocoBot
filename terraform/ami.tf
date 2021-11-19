resource "aws_instance" "locotroco_instance"{
    ami = "ami-06d79c60d7454e2af"
    instance_type = "t2.micro"
    tags = {
        Name = "LocotrocoBot_instance${var.test}"
    }
    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ubuntu"
      private_key = "locotrocobot-discord"
      timeout     = "4m"
   }
}

variable "test"{
    type = string
    description = "To create test enviroment"
    validation{
        condition = (var.test == "_test") || (var.test == "")
        error_message = "Only can use _test or empty string."
    }
}