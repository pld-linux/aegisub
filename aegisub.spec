# TODO
# - unvendor vendor/luabins
# - unvendor vendor/luajit
# - unvendor vendor/universalchardet
# - our cxxflags

# Conditional build:
%bcond_without	ffms2	# build ffms2 A/V provider

Summary:	Subtitle editor
Summary(pl.UTF-8):	Edytor napisów
Name:		aegisub
Version:	3.2.2
Release:	16
License:	BSD
Group:		X11/Applications
Source0:	http://ftp.aegisub.org/pub/releases/%{name}-%{version}.tar.xz
# Source0-md5:	d80e852c34811add358c06d77f5cd40d
Patch0:		pthread.patch
Patch1:		%{name}-icu.patch
Patch2:		%{name}-icu64.patch
Patch3:		%{name}-boost-1.70.patch
Patch4:		cflags.patch
Patch5:		make-4.3.patch
URL:		http://www.aegisub.org/
# AC_AGI_COMPILE tries to run test program which tries to open device and most likely fails
#BuildRequires:	OpenAL-devel >= 0.0.8
BuildRequires:	OpenGL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.50.0
%{?with_ffms2:BuildRequires:	ffms2-devel >= 2.16}
BuildRequires:	fftw3-devel >= 3.3
BuildRequires:	fontconfig-devel >= 1:2.4
# pkgconfig(freetype2) >= 9.7.0
BuildRequires:	freetype-devel >= 1:2.1.9
BuildRequires:	gettext-tools
BuildRequires:	hunspell-devel >= 1.2.0
BuildRequires:	intltool
BuildRequires:	libass-devel >= 0.9.7
BuildRequires:	libicu-devel >= 4.8.1.1
BuildRequires:	libstdc++-devel
BuildRequires:	lua51-devel
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	portaudio-devel >= 19
BuildRequires:	pulseaudio-devel >= 0.5
BuildRequires:	tar >= 1:1.22
BuildRequires:	wxGTK2-unicode-gl-devel >= 3.0.0
BuildRequires:	wxWidgets-devel >= 3.0.0
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	ffms2 >= 2.16
Requires:	fftw3 >= 3.3
Requires:	fontconfig-libs >= 1:2.4
Requires:	freetype >= 1:2.1.9
Requires:	hunspell >= 1.2.0
Requires:	libass >= 0.9.7
Requires:	libicu >= 4.8.1.1
Requires:	pulseaudio-libs >= 0.5
# due to luajit usage
ExclusiveArch:	%{ix86} %{x8664} arm mips ppc
# missing atomic_ops
ExcludeArch:	i386 i486
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Aegisub is an advanced subtitle editor for Windows, and UNIX-like
systems, such as Linux, Mac OS X and BSD. It is open source software
and free for any use.

Aegisub natively works with the Advanced SubStation Alpha format
(aptly abbreviated ASS) which allows for many advanced effects in the
subtitles, apart from just basic timed text. Aegisubs goal is to
support using these advanced functions with ease.

%description -l pl.UTF-8
Aegisub to zaawansowany edytor napisów dla Windows oraz systemów
uniksowych, takich jak Linux, Mac OS X czy BSD. Jest to program o
otwartych źródłach, darmowy do dowolnego użytku.

Aegisub działa natywnie na formacie Advanced SubStation Alpha (w
stosownym skrócie ASS), pozwalającym na wiele zaawansowanych efektów w
napisach, poza samym powiązaniem z czasem. Celem Aegisubs jest łatwa
obsługa tych zaawansowanych funkcji.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%{__mv} vendor{,.keep}
mkdir vendor
%{__mv} vendor.keep/{luabins,luajit,universalchardet} vendor

%build
%{__aclocal} -I m4macros
%{__autoconf}
%{__autoheader}
%configure \
	--disable-update-checker \
	%{__with_without ffms2} \
	--without-oss \
	--with-player-audio=PulseAudio \
	--with-wx-config=wx-gtk2-unicode-config

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -s %{name}-3.2 $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{fr_FR,fr}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{pt_PT,pt}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr_RS,sr}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr_RS,sr}@latin
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{uk_UA,uk}

%find_lang %{name}-32

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}-32.lang
%defattr(644,root,root,755)
%doc LICENCE README.md
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-3.2
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*
