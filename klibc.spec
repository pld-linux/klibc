#
# Conditional build:
%bcond_without	dist_kernel	# build without distribution kernel-headers
#
Summary:	Minimalistic libc subset for use with initramfs
Summary(pl):	Zminimalizowany podzbiór biblioteki C do u¿ywania z initramfs
Name:		klibc
Version:	0.193
Release:	1
License:	BSD
Group:		Libraries
Source0:	ftp://ftp.kernel.org/pub/linux/libs/klibc/%{name}-%{version}.tar.bz2
# Source0-md5:	d2616bbc5762dc1f2f9ebd87b597644e
Patch0:		%{name}-ksh-quotation.patch
Patch1:		%{name}-dirent.patch
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
ln -sf %{_kernelsrcdir}/include/linux include/linux

%{__make} \
	CC=%{__cc} \
	OPTFLAGS="%{rpmcflags} -Os -fomit-frame-pointer -falign-functions=0 \
		-falign-jumps=0 -falign-loops=0 -ffreestanding"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/klibc
install -d $RPM_BUILD_ROOT%{_libdir}/klibc/bin-{shared,static}

cp -a include/* $RPM_BUILD_ROOT%{_includedir}/klibc
install klibc/libc.* klibc/crt0.o	$RPM_BUILD_ROOT%{_libdir}/klibc

install utils/shared/* $RPM_BUILD_ROOT%{_libdir}/klibc/bin-shared
install utils/static/* $RPM_BUILD_ROOT%{_libdir}/klibc/bin-static

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/klibc
%attr(755,root,root) %{_libdir}/klibc/*.so
%{_libdir}/klibc/*.[ao]
%{_includedir}/klibc

%files utils-shared
%defattr(644,root,root,755)
%dir %{_libdir}/klibc/bin-shared
%attr(755,root,root) %{_libdir}/klibc/bin-shared/*

%files utils-static
%defattr(644,root,root,755)
%dir %{_libdir}/klibc/bin-static
%attr(755,root,root) %{_libdir}/klibc/bin-static/*
