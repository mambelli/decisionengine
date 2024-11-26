# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# RPM package for HEPCloud DEcisionengine pre-requisites

# Disable shebang mangling (see GHI#436)
%undefine __brp_mangle_shebangs

# Release Candidates NVR format
#%define release 0.1.rc1
# Official Release NVR format
#%define release 2

%define version __HCDE_RPM_VERSION__
%define release __HCDE_RPM_RELEASE__

%define decisionengine_home %{_localstatedir}/lib/decisionengine

#%define frontend_xml frontend.xml
#%define factory_xml glideinWMS.xml
%define condor_dir %{_localstatedir}/lib/gwms-factory/condor
%define systemddir %{_prefix}/lib/systemd/system

Name:           decisionengine-deps
Version:        %{version}
Release:        %{release}%{?dist}
Summary:        HEPCloud DecisionEngine dependencies
License:        Apache-2.0
URL:            http://https://hepcloud.github.io/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

#Source:         creation/templates/frontend_startup_sl7
#Source1:        creation/templates/factory_startup_sl7

BuildRequires: python3 >= 3.9
BuildRequires: python3-devel
BuildRequires: git
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: swig
#BuildRequires: python3-setuptools python3-wheel rpm-build

%description
The HEPCloud DecisionEngine provides a simple way to access the Grid, Cloud and HPC
resources through a dynamic condor pool of grid-submitted resources.
HEPCloud DecisionEngine is installed via PIP.
These RPMs provide all the pre-requisites and necessary setup.

%package deps
Summary: The HEPCloud Decision Engine dependencies.
Requires: python3 >= 3.9
Requires: postgresql
Requires: postgresql-server
Requires: postgresql-devel
Requires: httpd
Requires: podman
Requires: python3-cryptography
Requires: python3-pip
Requires: gettext
%description deps
This subpackage includes all the RPM dependencied for the HEPCloud Decision Engine Framework.


%package modules-deps
Summary: The HEPCloud Decision Engine Modules dependencies.
Requires: python3 >= 3.9
Requires: decisionengine-deps = %{version}-%{release}
Requires: glideinwms-vofrontend-libs
Requires: glideinwms-vofrontend-glidein
Requires: glideinwms-userschedd
Requires: glideinwms-usercollector
Requires: glideinwms-vofrontend-core
Requires: glideinwms-vofrontend-httpd
Requires: 
Requires: 
Requires: 
Requires: 
%description modules-deps
This subpackage includes all the RPM dependencied for the HEPCloud Decision Engine Modules.


%prep
%setup -q -n decisionengine
# Apply the patches here if any
#%patch -P 0 -p1


%build
#cp %{SOURCE7} .
#chmod 700 chksum.sh
#./chksum.sh v%{version}-%{release}.osg etc/checksum.frontend "CVS doc .git .gitattributes poolwatcher factory/check* factory/glideFactory* factory/test* factory/manage* factory/stop* factory/tools creation/create_glidein creation/reconfig_glidein creation/info_glidein creation/lib/cgW* creation/web_base/factory*html creation/web_base/collector_setup.sh creation/web_base/condor_platform_select.sh creation/web_base/condor_startup.sh creation/web_base/create_mapfile.sh creation/web_base/singularity_setup.sh creation/web_base/singularity_wrapper.sh creation/web_base/singularity_lib.sh creation/web_base/gconfig.py creation/web_base/glidein_startup.sh creation/web_base/job_submit.sh creation/web_base/local_start.sh creation/web_base/setup_x509.sh creation/web_base/update_proxy.py creation/web_base/validate_node.sh chksum.sh etc/checksum* unittests build"
#./chksum.sh v%{version}-%{release}.osg etc/checksum.factory "CVS doc .git .gitattributes poolwatcher frontend/* creation/reconfig_glidein creation/clone_glidein creation/lib/cgW* creation/web_base/factory*html creation/web_base/collector_setup.sh creation/web_base/condor_platform_select.sh creation/web_base/condor_startup.sh creation/web_base/create_mapfile.sh creation/web_base/singularity_setup.sh creation/web_base/singularity_wrapper.sh creation/web_base/singularity_lib.sh creation/web_base/gconfig.py creation/web_base/glidein_startup.sh creation/web_base/job_submit.sh creation/web_base/local_start.sh creation/web_base/setup_x509.sh creation/web_base/update_proxy.py creation/web_base/validate_node.sh chksum.sh etc/checksum* unittests build creation/lib/matchPolicy*"

%install
rm -rf $RPM_BUILD_ROOT

# Set the Python version
%global __python %{__python3}

# TODO: Check if some of the following are needed
# seems never used
# %define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%d.%d'%v")

# From http://fedoraproject.org/wiki/Packaging:Python
# Assuming python3_sitelib and python3_sitearch are defined, not supporting RHEL < 7 or old FC
# Define python_sitelib

#Change src_dir in reconfig_Frontend
#sed -i "s/WEB_BASE_DIR *=.*/WEB_BASE_DIR = \"\/var\/lib\/gwms-frontend\/web-base\"/" creation/reconfig_frontend

#Create the RPM startup files (init.d) from the templates
#creation/create_rpm_startup . frontend_initd_startup_template factory_initd_startup_template %{SOURCE1} %{SOURCE6}

# Create some directories
install -d $RPM_BUILD_ROOT%{decisionengine_home}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/decisionengine
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/decisionengine

%clean
rm -rf $RPM_BUILD_ROOT


%pre deps
# Add the "decisionengine" user and group if they do not exist
getent group decisionengine >/dev/null || groupadd -r decisionengine
getent passwd decisionengine >/dev/null || \
       useradd -r -g decisionengine -d %{decisionengine_home} \
	-c "HEPCloud Deciosion Engine user" -s /sbin/nologin decisionengine
# If the decisionengine user already exists make sure it is part of decisionengine group
usermod --append --groups decisionengine decisionengine >/dev/null


%files deps
%defattr(-,decisionengine,decisionengine,-)
%dir %{decisionengine_home}
%dir %{_sysconfdir}/decisionengine
%attr(-, decisionengine, decisionengine) %dir %{_localstatedir}/log/decisionengine

%files modules-deps
