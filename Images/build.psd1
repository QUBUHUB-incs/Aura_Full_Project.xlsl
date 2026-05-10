# Create VM
VBoxManage createvm --name "DevVM" --register

# Set OS type
VBoxManage modifyvm "DevVM" --ostype Ubuntu_64 --memory 40966 --cpus 2

# Create disk
VBoxManage createmedium disk --filename "DevVM.vdi" --size 20000

# Attach disk + ISO (replace path)
VBoxManage storagectl "DevVM" --name "SATA" --add sata
VBoxManage storageattach "DevVM" --storagectl "SATA" --port 0 --device 0 --type hdd --medium "DevVM.vdi"
VBoxManage storageattach "DevVM" --storagectl "SATA" --port 1 --device 0 --type dvddrive --medium "ubuntu.iso"

# Start VM
VBoxManage startvm "DevVM"
