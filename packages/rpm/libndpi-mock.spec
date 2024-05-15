Summary: L7 DPI library
Name: libndpi
Version: 3.4.0
Release: %{__release}%{?dist}
License: LGPL
Group: Networking/Utilities
URL: http://www.ntop.org/products/deep-packet-inspection/ndpi/
Source: libndpi-%{version}.tgz
Packager: David Vanhoucke <dvanhoucke@redborder.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}-root

BuildRequires: autoconf automake libtool pkg-config autoconf-archive libpcap-devel

AutoReqProv: no

Provides: libndpi.so.3()(64bit)

%define debug_package %{nil}

# Make sure .build-id is not part of the package
%define _build_id_links none

%description
nDPI Open and Extensible LGPLv3 Deep Packet Inspection Library.

%package dev
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-dev.

%prep

%setup -q

# Execution order:
# install:    pre -> (copy) -> post
# upgrade:    pre -> (copy) -> post -> preun (old) -> (delete old) -> postun (old)
# un-install:                          preun       -> (delete)     -> postun

%pre

%build
PATH=/usr/bin:/bin:/usr/sbin:/sbin

%define includedir /usr/include/libndpi
%define libdir     /usr/lib64
%define bindir     /usr/bin

./autogen.sh
export LD_LIBRARY_PATH=%{libdir}
./configure --prefix=/usr --exec-prefix=/usr --bindir=%{bindir} --sbindir=%{bindir} --libdir=%{libdir} --includedir=%{includedir}

%install
PATH=/usr/bin:/bin:/usr/sbin:/sbin
if [ -d $RPM_BUILD_ROOT ]; then
	\rm -rf $RPM_BUILD_ROOT
fi
mkdir -p $RPM_BUILD_ROOT%{includedir}
mkdir -p $RPM_BUILD_ROOT%{libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{bindir}

make DESTDIR=$RPM_BUILD_ROOT install;
cp libndpi.pc $RPM_BUILD_ROOT%{libdir}/pkgconfig
#cd $RPM_BUILD_ROOT%{libdir}/; ln -s libndpi.so.3.4.0 libndpi.so.3; cd -
#cd $RPM_BUILD_ROOT%{libdir}/; ln -s libndpi.so.3.4.0 libndpi.so; cd -
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
cp packages/etc/ld.so.conf.d/ndpi.conf $RPM_BUILD_ROOT/etc/ld.so.conf.d
rm -rf $RPM_BUILD_ROOT/usr/sbin/ndpi
strip $RPM_BUILD_ROOT%{bindir}/*
rm -fr %{buildroot}%{includedir}/ndpi_win32.h

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%{libdir}/libndpi.so
%{libdir}/libndpi.so.3
%{libdir}/libndpi.so.3.4.0
/usr/bin/ndpiReader
/usr/share/ndpi/ndpiCustomCategory.txt
/usr/share/ndpi/ndpiProtos.txt
/etc/ld.so.conf.d/ndpi.conf
%{libdir}/pkgconfig/libndpi.pc

%preun

%files dev
%defattr(-,root,root,-)

%{includedir}
%{libdir}/libndpi.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Thu Apr 25 2024 David Vanhoucke <dvanhoucke@redborder.com>
- adaption for mock rpm build
* Mon Nov 19 2018 Alfredo Cardigliano <cardigliano@ntop.org> 2.5
- Initial package version
