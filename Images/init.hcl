source "virtualbox-iso" "ubuntu" {
  iso_url      = "ubuntu.iso"
  iso_checksum = "none"
  ssh_username = "ubuntu"
  ssh_password = "ubuntu"
}

build {
  sources = ["source.virtualbox-iso.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt update",
      "sudo apt install -y nginx docker.dev , docker.io, docker.vm",
      "echo 'Setup complete'"
    ]
  }
}
