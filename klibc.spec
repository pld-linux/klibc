Summary:	Minimalistic libc subset for use with initramfs
Summary(pl):	Zminimalizowany podzbi�r bibliteki C do u�ywa z initramfs
Name:		klibc
Version:	0.22
Release:	1
License:	BSD
Group:		Libraries
Source0:	ftp://ftp.kernel.org/pub/linux/libs/klibc/%{name}-%{version}.tar.bz2
BuildRequires:	kernel-source >= 2.4
BuildRequires:	perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define no_install_post_strip 1

%description
klibc, what is intended to be a minimalistic libc subset for use with
initramfs. It is deliberately written for small size, minimal
entaglement and portability, not speed. It is definitely a work in
progress, and a lot of things are still missing.

%description -l pl
klibc w zamierzeniu ma by� minimalistycznym podzbiorem biblioteki libc
do u�ycia z initramfs. Celem jest minimalizacja, przenaszalno�� ale
nie szybko��. klibc jest rozwijan� bibliotek� w zwi�zku z czym nadal
brakuje wielu rzeczy.

%prep
%setup -q

%build
ln -s %{_kernelsrcdir} linux

# 32 bit archs
%ifarch %{ix86} sparc sparc32 ppc
ln -sf bits32 include/bitsize
%endif
# 64 bit archs
%ifarch alpha sparc64 ppc64
ln -sf bits64 include/bitsize
%endif

%{__make} \
%ifarch %{ix86}
	ARCH=i386 \
%else
	ARCH=%{_target_cpu} \
%endif
	OPTFLAGS="%{rpmcflags} -Os -fomit-frame-pointer -falign-functions=0 \
		-falign-jumps=0 -falign-loops=0"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/klibc
install -d $RPM_BUILD_ROOT%{_libdir}/klibc

cp -a include/* $RPM_BUILD_ROOT%{_includedir}/klibc
install libc.* crt0.o	$RPM_BUILD_ROOT%{_libdir}/klibc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_includedir}/klibc
%dir %{_libdir}/klibc
%{_libdir}/klibc/*.[ao]
%attr(755,root,root) %{_libdir}/klibc/*.so
