Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-18.04"
  config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "private_network", ip: "55.55.55.5"
  # config.vm.network "forwarded_port", guest: 8000, host: 8081, host_ip: "127.0.0.1"
  # config.vm.synced_folder ".", "/home/vagrant/code"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "1024"
    vb.name = "monticello"
  end
end
