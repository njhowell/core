# encoding: utf-8
# -*- mode: ruby -*-
# vi: set ft=ruby :# Box / OS
VAGRANT_BOX = 'ubuntu/focal64'# Memorable name for your
VM_NAME = 'hassdev'# VM User — 'vagrant' by default
VM_USER = 'vagrant'# Username on your Mac

# VM_PORT = 8080
Vagrant.configure(2) do |config|  # Vagrant box from Hashicorp
  config.vm.box = VAGRANT_BOX
  
  # Actual machine name
  config.vm.hostname = VM_NAME  # Set VM name in Virtualbox
  config.vm.provider "virtualbox" do |v|
    v.name = VM_NAME
    v.memory = 4096
  end  #DHCP — comment this out if planning on using NAT instead
  config.vm.network "public_network"  # # Port forwarding — uncomment this to use NAT instead of DHCP
  #config.vm.network "forwarded_port", guest: 8123, host: 8123  # Sync folder  
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y git python3-pip python3-dev python3-venv autoconf libssl-dev libxml2-dev libxslt1-dev libjpeg-dev libffi-dev libudev-dev zlib1g-dev pkg-config libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev libavfilter-dev ffmpeg python3-virtualenv
    apt-get update
    apt-get upgrade -y
    apt-get autoremove -y
  SHELL
end