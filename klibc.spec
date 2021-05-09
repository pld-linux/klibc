#
# TODO:
#    - warning: Installed (but unpackaged) file(s) found:
#               /usr/lib/klibc/libc.so.hash
#
# Conditional build:
%bcond_without	dist_kernel	# build without distribution kernel-headers
%bcond_with	verbose		# verbose build
#
Summary:	Minimalistic libc subset for use with initramfs
Summary(pl.UTF-8):	Zminimalizowany podzbiór biblioteki C do używania z initramfs
Name:		klibc
Version:	2.0.9
Release:	1
License:	BSD/GPL
Group:		Libraries
Source0:	https://www.kernel.org/pub/linux/libs/klibc/2.0/%{name}-%{version}.tar.xz
# Source0-md5:	7554a9759ae71e9ba3729991c8ae7f63
Patch0:		%{name}-klcc.patch
URL:		https://lists.zytor.com/klibc/
# ld.bfd binary
BuildRequires:	binutils >= 2.20.51.0.6
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	linux-libc-headers >= 7:2.6.24-1
BuildRequires:	perl-base
BuildRequires:	perl-modules
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%description
klibc, what is intended to be a minimalistic libc subset for use with
initramfs. It is deliberately written for small size, minimal
entaglement and portability, not speed. It is definitely a work in
progress, and a lot of things are still missing.

%description -l pl.UTF-8
klibc w zamierzeniu ma być minimalistycznym podzbiorem biblioteki libc
do użycia z initramfs. Celem jest minimalizacja, przenośność ale nie
szybkość. klibc jest rozwijaną biblioteką w związku z czym nadal
brakuje wielu rzeczy.

%package devel
Summary:	Development files for klibc
Summary(pl.UTF-8):	Pliki dla programistów klibc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	binutils
Requires:	linux-libc-headers >= 7:2.6.24-1

%description devel
Small libc for building embedded applications - development files.

%description devel -l pl.UTF-8
Mała libc do budowania aplikacji wbudowanych - pliki dla programistów.

%package static
Summary:	Static klibc libraries
Summary(pl.UTF-8):	Biblioteki statyczne klibc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static klibc libraries.

%description static -l pl.UTF-8
Biblioteki statyczne klibc.

%package utils-shared
Summary:	Utilities dynamically linked with klibc
Summary(pl.UTF-8):	Narzędzia dynamicznie zlinkowane z klibc
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description utils-shared
Utilities dynamically linked with klibc.

%description utils-shared -l pl.UTF-8
Narzędzia dynamicznie zlinkowane z klibc.

%package utils-shared-debug
Summary:	Utilities dynamically linked with klibc (unstripped)
Summary(pl.UTF-8):	Narzędzia dynamicznie zlinkowane z klibc (z informacjami dla debuggera)
Group:		Base
Requires:	%{name}-utils-shared = %{version}-%{release}

%description utils-shared-debug
Utilities dynamically linked with klibc.

Programs in this package have debugging information not stripped.

%description utils-shared-debug -l pl.UTF-8
Narzędzia dynamicznie zlinkowane z klibc.

Programy zawarte w tym pakiecie zawierają informacje dla debuggera.

%package utils-static
Summary:	Utilities statically linked with klibc
Summary(pl.UTF-8):	Narzędzia statycznie zlinkowane z klibc
Group:		Base

%description utils-static
Utilities staticly linked with klibc.

%description utils-static -l pl.UTF-8
Narzędzia statycznie zlinkowane z klibc.

%package utils-static-debug
Summary:	Utilities statically linked with klibc (unstripped)
Summary(pl.UTF-8):	Narzędzia statycznie zlinkowane z klibc (z informacjami dla debuggera)
Group:		Base
Requires:	%{name}-utils-static = %{version}-%{release}

%description utils-static-debug
Utilities staticly linked with klibc.

Programs in this package have debugging information not stripped.

%description utils-static-debug -l pl.UTF-8
Narzędzia statycznie zlinkowane z klibc.

Programy zawarte w tym pakiecie zawierają informacje dla debuggera.

%prep
%setup -q
%patch0 -p1

%build
cd usr/include
ln -sf /usr/include/asm .
ln -sf /usr/include/asm-generic .
%ifarch sparc64
ln -sf /usr/include/asm-sparc .
ln -sf /usr/include/asm-sparc64 .
%endif
ln -sf /usr/include/linux .
# early-userspace needs acces to e.g. uvesafb.h.
ln -sf /usr/include/video .

cd ../..
install -d linux
ln -sf ../usr/include linux/include

%{__make} \
	ARCH=%{_target_base_arch} \
	HOSTCC="%{__cc}" \
	CC="%{__cc}" \
	LD="ld.bfd" \
	rpm_prefix=%{_prefix} \
	rpm_bindir=%{_bindir} \
	rpm_includedir=%{_includedir}/klibc \
	rpm_libdir=%{_libdir} \
	SHLIBDIR=/%{_lib} \
	%{?with_verbose:KBUILD_VERBOSE=1} \
	OPTFLAGS="%{rpmcflags} -Os -fomit-frame-pointer -falign-functions=0 \
		-falign-jumps=0 -falign-loops=0 -ffreestanding"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}
install -d $RPM_BUILD_ROOT%{_includedir}/klibc
install -d $RPM_BUILD_ROOT%{_libdir}/klibc/bin-{shared,static}

cp -a usr/include/* $RPM_BUILD_ROOT%{_includedir}/klibc
install klcc/klcc -D $RPM_BUILD_ROOT%{_bindir}/klcc
install klcc/klcc.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/klcc.1
install usr/klibc/libc.* usr/klibc/arch/%{_target_base_arch}/crt0.o usr/klibc/interp.o $RPM_BUILD_ROOT%{_libdir}/klibc
install usr/klibc/klibc-*.so $RPM_BUILD_ROOT/%{_lib}
install usr/dash/shared/sh $RPM_BUILD_ROOT%{_libdir}/klibc/bin-shared
install usr/dash/shared/sh.g $RPM_BUILD_ROOT%{_libdir}/klibc/bin-shared
install usr/dash/static/sh $RPM_BUILD_ROOT%{_libdir}/klibc/bin-static
install usr/dash/static/sh.g $RPM_BUILD_ROOT%{_libdir}/klibc/bin-static
install usr/gzip/{gunzip,gzip,gzip.g,zcat} $RPM_BUILD_ROOT%{_libdir}/klibc/bin-static
install usr/kinit/*/shared/* $RPM_BUILD_ROOT%{_libdir}/klibc/bin-shared
install usr/kinit/*/static/* $RPM_BUILD_ROOT%{_libdir}/klibc/bin-static
install usr/utils/shared/* $RPM_BUILD_ROOT%{_libdir}/klibc/bin-shared
install usr/utils/static/* $RPM_BUILD_ROOT%{_libdir}/klibc/bin-static

ln -s %{_libdir}/klibc/bin-shared $RPM_BUILD_ROOT%{_libdir}/klibc/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/klibc-*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/klcc
%{_includedir}/klibc
%dir %{_libdir}/klibc
%attr(755,root,root) %{_libdir}/klibc/*.so
%{_libdir}/klibc/*.o
%{_mandir}/man1/klcc.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/klibc/*.a

%files utils-shared
%defattr(644,root,root,755)
%{_libdir}/klibc/bin
%dir %{_libdir}/klibc/bin-shared
%attr(755,root,root) %{_libdir}/klibc/bin-shared/*
%exclude %{_libdir}/klibc/bin-shared/*.g

%files utils-shared-debug
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/klibc/bin-shared/*.g

%files utils-static
%defattr(644,root,root,755)
%dir %{_libdir}/klibc/bin-static
%attr(755,root,root) %{_libdir}/klibc/bin-static/*
%exclude %{_libdir}/klibc/bin-static/*.g

%files utils-static-debug
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/klibc/bin-static/*.g
