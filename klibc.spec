#
# Conditional build:
%bcond_without	dist_kernel	# build without distribution kernel-headers
#
Summary:	Minimalistic libc subset for use with initramfs
Summary(pl):	Zminimalizowany podzbiór biblioteki C do u¿ywania z initramfs
Name:		klibc
Version:	1.0
Release:	1
License:	BSD/GPL
Group:		Libraries
Source0:	http://www.kernel.org/pub/linux/libs/klibc/%{name}-%{version}.tar.bz2
# Source0-md5:	daaa233fb7905cbe110896fcad9bec7f
Patch0:		%{name}-ksh-quotation.patch
Patch1:		%{name}-klcc.patch
URL:		http://www.zytor.com/mailman/listinfo/klibc/
%{?with_dist_kernel:BuildRequires:	kernel-headers >= 2.4}
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRequires:	perl-base
%{?with_dist_kernel:Requires:	kernel-headers >= 2.4}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%description
klibc, what is intended to be a minimalistic libc subset for use with
initramfs. It is deliberately written for small size, minimal
entaglement and portability, not speed. It is definitely a work in
progress, and a lot of things are still missing.

%description -l pl
klibc w zamierzeniu ma byæ minimalistycznym podzbiorem biblioteki libc
do u¿ycia z initramfs. Celem jest minimalizacja, przeno¶no¶æ ale nie
szybko¶æ. klibc jest rozwijan± bibliotek± w zwi±zku z czym nadal
brakuje wielu rzeczy.

%package utils-shared
Summary:	Utilities dynamically linked with klibc
Summary(pl):	Narzêdzia dynamicznie zlinkowane z klibc
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description utils-shared
Utilities dynamically linked with klibc.

%description utils-shared -l pl
Narzêdzia dynamicznie zlinkowane z klibc.

%package utils-static
Summary:	Utilities statically linked with klibc
Summary(pl):	Narzêdzia statycznie zlinkowane z klibc
Group:		Base

%description utils-static
Utilities staticly linked with klibc.

%description utils-static -l pl
Narzêdzia statycznie zlinkowane z klibc.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -rf include/{asm,asm-generic,linux}
ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
ln -sf %{_kernelsrcdir}/include/asm-generic include/asm-generic
cp -ar %{_kernelsrcdir}/include/linux include/linux
ln -sf %{_kernelsrcdir}/include/linux/autoconf-up.h include/linux/autoconf.h

%{__make} \
%if 0
	ARCH=%{_target_base_arch} \
	CROSS=%{_target_base_arch}-pld-linux- \
%else
	CC=%{__cc} \
%endif
	bindir=%{_bindir} \
	includedir=%{_includedir}/klibc \
	libdir=%{_libdir} \
	prefix=%{_prefix} \
	OPTFLAGS="%{rpmcflags} -Os -fomit-frame-pointer -falign-functions=0 \
		-falign-jumps=0 -falign-loops=0 -ffreestanding"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/klibc
install -d $RPM_BUILD_ROOT%{_libdir}/klibc/bin-{shared,static}

cp -a include/* $RPM_BUILD_ROOT%{_includedir}/klibc
install klcc -D $RPM_BUILD_ROOT%{_bindir}/klcc
install klcc.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/klcc.1
install klibc/libc.* klibc/crt0.o klibc/interp.o $RPM_BUILD_ROOT%{_libdir}/klibc
install utils/shared/* $RPM_BUILD_ROOT%{_libdir}/klibc/bin-shared
install utils/static/* $RPM_BUILD_ROOT%{_libdir}/klibc/bin-static

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/klcc
%{_includedir}/klibc
%dir %{_libdir}/klibc
%attr(755,root,root) %{_libdir}/klibc/*.so
%{_libdir}/klibc/*.[ao]
%{_mandir}/man1/*

%files utils-shared
%defattr(644,root,root,755)
%dir %{_libdir}/klibc/bin-shared
%attr(755,root,root) %{_libdir}/klibc/bin-shared/*

%files utils-static
%defattr(644,root,root,755)
%dir %{_libdir}/klibc/bin-static
%attr(755,root,root) %{_libdir}/klibc/bin-static/*
