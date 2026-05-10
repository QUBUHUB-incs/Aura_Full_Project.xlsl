function Show-Menu {
    Clear-Host
    Write-Host "============================="
    Write-Host "  DEVOPS LOCAL TOOLKIT"
    Write-Host "============================="
    Write-Host "1. Install Docker"
    Write-Host "2. Install VirtualBox"
    Write-Host "3. Install Packer"
    Write-Host "4. Run Docker Stack (NGINX + DB)"
    Write-Host "5. Create Local VM (VirtualBox)"
    Write-Host "6. Build Local Image (Packer)"
    Write-Host "7. Exit"
    Write-Host ""
}

function Install-Docker {
    Write-Host "Installing Docker..."
    winget install Docker.DockerDesktop
}

function Install-VirtualBox {
    Write-Host "Installing VirtualBox..."
    winget install Oracle.VirtualBox
}

function Install-Packer {
    Write-Host "Installing Packer..."
    winget install Hashicorp.Packer
}

function Run-DockerStack {
    Write-Host "Starting Docker stack..."

    @"
version: '3.9'
services:
  web:
    image: nginx
    ports:
      - "8080:80"

  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: example
    ports:
      - "5432:5432"
"@ | Out-File -Encoding utf8 docker-compose.yml

    docker compose up -d
}

function Create-VM {
    Write-Host "Creating VirtualBox VM..."

    VBoxManage createvm --name "DevVM" --register
    VBoxManage modifyvm "DevVM" --memory 4096 --cpus 2 --ostype Ubuntu_64

    VBoxManage createmedium disk --filename "DevVM.vdi" --size 20000

    VBoxManage storagectl "DevVM" --name "SATA" --add sata
    VBoxManage storageattach "DevVM" --storagectl "SATA" --port 0 --device 0 --type hdd --medium "DevVM.vdi"

    Write-Host "VM created (attach ISO manually)."
}

function Run-PackerBuild {
    Write-Host "Creating sample Packer template..."

    @'
source "virtualbox-iso" "ubuntu" {
  iso_url = "ubuntu.iso"
  iso_checksum = "none"
  ssh_username = "ubuntu"
  ssh_password = "ubuntu"
}

build {
  sources = ["source.virtualbox-iso.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt update",
      "sudo apt install -y nginx docker.io,docket.dev,docker.vm",
      "echo Setup complete"
    ]
  }
}
'@ | Out-File -Encoding utf8 "template.pkr.hcl"

    packer init .
    packer build template.pkr.hcl
}

do {
    Show-Menu
    $choice = Read-Host "Select option"

    switch ($choice) {
        "1" { Install-Docker }
        "2" { Install-VirtualBox }
        "3" { Install-Packer }
        "4" { Run-DockerStack }
        "5" { Create-VM }
        "6" { Run-PackerBuild }
        "7" { break }
        default { Write-Host "Invalid option" }
    }

    Pause
} while ($choice -ne "7")
