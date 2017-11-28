%define lib_name libzmq4
%bcond_without pgm

# To build with draft APIs, use "--with drafts" in rpmbuild for local builds or add
#   Macros:
#   %_with_drafts 1
# at the BOTTOM of the OBS prjconf
%bcond_with drafts
%if %{with drafts}
%define DRAFTS yes
%else
%define DRAFTS no
%endif
%define SYSTEMD_UNIT_DIR %(pkg-config --variable=systemdsystemunitdir systemd)

Name:           zeromq
Version:        4.2.0+20150120be23e699c9
Release:        1%{?dist}
Summary:        Software library for fast, message-based applications

Group:          System Environment/Libraries
License:        LGPLv3+ with exceptions
URL:            http://www.zeromq.org
# VCS:          git:git://github.com/zeromq/libzmq.git
# VCS:          git:git://github.com/zeromq/zeromq3-x.git
#####
#Source0:        http://download.zeromq.org/zeromq-%%{version}.tar.gz
#####
# created with:
# git clone git:http://github.com/zeromq/libzmq.git && cd limzmq
# git archive --format=tar.gz --prefix=zeromq-3.2.0/ 1ef63bc2adc3d50 > zeromq-3.2.0.tar.gz
#Source0:        zeromq-%%{version}.tar.gz
#####
# rc's
Source0:        %{name}-%{version}.tar.gz
#####
BuildRequires:  glib2-devel
BuildRequires:  libuuid-devel
BuildRequires:  gcc-c++
BuildRequires:  libsodium-devel
BuildRequires:  pkg-config
BuildRequires:  libtool
BuildRequires:  autoconf
BuildRequires:  automake
# documentation
BuildRequires:  asciidoc
BuildRequires:  xmlto
BuildRequires:  xz
#TODO: add openpgm-devel to obs.roz.lab.etn.com
# % if % {with pgm}
#BuildRequires:  openpgm-devel
# % endif


%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the ZeroMQ shared library for versions 3.x.

%package -n %{lib_name}
Summary:        Shared Library for ZeroMQ

%description -n %{lib_name}
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialised messaging middleware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging patterns,
message filtering (subscriptions), seamless access to multiple transport
protocols and more.

This package holds the shared library part of the ZeroMQ package.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{lib_name} = %{version}-%{release}
Conflicts:      zeromq-devel


%description devel
The %{name}-devel package contains libraries and header files for 
developing applications that use %{name} 3.x.


%prep
%setup -q -n %{name}-%{version}/

# remove all files in foreign except Makefiles
rm -vf $(find foreign -type f | grep -v Makefile)
./autogen.sh
# Don't turn warnings into errors
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" \
    configure


%build
%configure \
            --disable-static \
            --with-pic
# % if %{with pgm}
#            --with-system-pgm \
# % endif
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

# remove *.la
rm %{buildroot}%{_libdir}/libzmq.la


# % check
#make check ||:


%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root,-)
%doc COPYING COPYING.LESSER
%{_libdir}/libzmq.so.*


%files
%exclude %{_bindir}/curve_keygen
%doc AUTHORS COPYING COPYING.LESSER NEWS
#%doc ChangeLog

%files devel
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/zmq*
#TODO: add asciidoc if you want to have man pages
# % {_mandir}/man3/zmq*.3*
# % {_mandir}/man7/zmq*.7*
%{_mandir}/man*/*.?.gz

%changelog
