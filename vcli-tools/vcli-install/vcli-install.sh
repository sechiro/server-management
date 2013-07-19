sudo yum install openssl-devel
sudo yum install perl-CPAN
sudo yum install libxml2-devel
sudo yum install uuid-perl # 必要ないかも
sudo yum install uuid-devel # 必要ないかも
sudo yum install libuuid-devel

sudo cpan UUID
sudo cpan XML::LibXML::Common
sudo cpan XML::LibXML

# Download and apply patch for VMware-vSphere-CLI-5.1.0-1060453.tar.gz
vcli_installer_path=/path/to/installer
patch -u $vcli_installer_path/vmware-install.pl < vmware-install.pl.patch
sudo $vcli_installer_path/vmware-install.pl
