# TODO
# - unvendor vendor/luabins
# - unvendor vendor/luajit
# - unvendor vendor/universalchardet
# - our cxxflags

# Conditional build:
%bcond_without	ffms2	# build ffms2 A/V provider

Summary:	Subtitle editor
Name:		aegisub
Version:	3.2.0
Release:	1
License:	BSD
Group:		X11/Applications
Source0:	http://ftp.aegisub.org/pub/releases/%{name}-%{version}.tar.xz
# Source0-md5:	914685eb87daf230ac8856ed81479b43
URL:		http://www.aegisub.net/
BuildRequires:	Mesa-libGL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.50
%{?with_ffms2:BuildRequires:	ffms2-devel}
BuildRequires:	fftw3-devel >= 3.3
BuildRequires:	fontconfig-devel >= 1:2.4
BuildRequires:	gettext-tools
BuildRequires:	hunspell-devel >= 1.2.0
BuildRequires:	intltool
BuildRequires:	libass-devel
BuildRequires:	libicu-devel
BuildRequires:	libstdc++-devel
BuildRequires:	lua51-devel
BuildRequires:	pkg-config >= 0.20
BuildRequires:	pulseaudio-devel >= 0.5
BuildRequires:	tar >= 1:1.22
BuildRequires:	wxGTK2-unicode-gl-devel
BuildRequires:	wxWidgets-devel >= 2.9.5
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Aegisub is an advanced subtitle editor for Windows, and UNIX-like
systems, such as Linux, Mac OS X and BSD. It is open source software
and free for any use.

Aegisub natively works with the Advanced SubStation Alpha format
(aptly abbreviated ASS) which allows for many advanced effects in the
subtitles, apart from just basic timed text. Aegisubs goal is to
support using these advanced functions with ease.

%prep
%setup -q

mv vendor{,.keep}
mkdir vendor
mv vendor.keep/{luabins,luajit,universalchardet} vendor

%build
%configure \
	--with-player-audio=PulseAudio \
	--disable-update-checker \
	--with-wx-config=wx-gtk2-unicode-config \
	%{__with_without ffms2} \
	--without-oss

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -s %{name}-3.2 $RPM_BUILD_ROOT%{_bindir}/%{name}

%find_lang %{name}-32

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-32.lang
%defattr(644,root,root,755)
%doc LICENCE
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-3.2
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*
