#
# Conditional build:
%bcond_without	dist_kernel	# build without distribution kernel-headers
#
Summary:	Minimalistic libc subset for use with initramfs
Summary(pl):	Zminimalizowany podzbiór biblioteki C do u¿ywania z initramfs
Name:		klibc
Version:	0.89
Release:	1
License:	BSD
Group:		Libraries
Source0:	ftp://ftp.kernel.org/pub/linux/libs/klibc/%{name}-%{version}.tar.bz2
# Source0-md5:	30ed2f7be1bf3327b531f8087c8ab9b6
URL:		http://www.zytor.com/mailman/listinfo/klibc/
%{?with_dist_kernel:BuildRequires:	kernel-headers >= 2.4}
BuildRequires:	perl-base
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

%prep
%setup -q

%build
ln -s %{_kernelsrcdir} linux

%{__make} \
	CC=%{__cc} \
	OPTFLAGS="%{rpmcflags} -Os -fomit-frame-pointer -falign-functions=0 \
		-falign-jumps=0 -falign-loops=0"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/klibc
install -d $RPM_BUILD_ROOT%{_libdir}/klibc

cp -a klibc/include/* $RPM_BUILD_ROOT%{_includedir}/klibc
install klibc/libc.* klibc/crt0.o	$RPM_BUILD_ROOT%{_libdir}/klibc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/klibc
%attr(755,root,root) %{_libdir}/klibc/*.so
%{_libdir}/klibc/*.[ao]
%{_includedir}/klibc
