#
# Conditional build:
%bcond_without	src		# build devel package with sources
%bcond_without	tests	# build without tests

Summary:	Client for keybase.io
Name:		keybase
Version:	1.0.18
Release:	1
License:	BSD
Group:		Applications
Source0:	https://github.com/keybase/client/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	31e00e18828e38d3d8eb53df43cb3c74
URL:		https://keybase.io/
BuildRequires:	golang >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/keybase/client

%description
Client for keybase.io.

%prep
%setup -qc

mv client-%{version}/{*.md,LICENSE} .

install -d src/$(dirname %{import_path})
mv client-%{version} src/%{import_path}

%build
export GOPATH=$(pwd)

%gobuild github.com/keybase/client/go/keybase

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p %{name} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/keybase
