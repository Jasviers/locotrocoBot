resource "aws_instance" "locotroco_instance"{
    ami = var.ami
    instance_type = var.instance_type

    tags = {
        Name = "${var.prefix}_locotrocoBot_instance"
    }

    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ubuntu"
      private_key = "locotrocobot-discord"
      timeout     = "4m"
   }
}
