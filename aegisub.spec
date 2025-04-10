# TODO
# - unvendor vendor/luabins
# - unvendor vendor/universalchardet
# - our cxxflags

# Conditional build:
%bcond_without	ffms2	# ffms2 A/V provider

Summary:	Subtitle editor
Summary(pl.UTF-8):	Edytor napisów
Name:		aegisub
Version:	3.4.2
Release:	1
License:	BSD
Group:		X11/Applications
#Source0Download: https://aegisub.org/downloads/
Source0:	https://github.com/TypesettingTools/Aegisub/releases/download/v%{version}/Aegisub-%{version}.tar.xz
# Source0-md5:	d60c9942d1c211b266e29fdde689e3e8
#Source0:	https://github.com/TypesettingTools/Aegisub/archive/v%{version}/Aegisub-%{version}.tar.gz
Patch0:		no-tests.patch
Patch2:		luajit-5.2.patch
URL:		https://aegisub.org/
BuildRequires:	OpenAL-devel >= 0.0.8
BuildRequires:	OpenGL-devel
BuildRequires:	alsa-lib-devel
# chrono, thread, locale, regex, system
BuildRequires:	boost-devel >= 1.70.0
%{?with_ffms2:BuildRequires:	ffms2-devel >= 2.22}
BuildRequires:	fftw3-devel >= 3.3
BuildRequires:	fontconfig-devel >= 1:2.4
BuildRequires:	gettext-tools >= 0.18.1
BuildRequires:	gmock-devel >= 1.14.0
BuildRequires:	gtest-devel >= 1.14.0
BuildRequires:	hunspell-devel >= 1.2.0
BuildRequires:	libass-devel >= 0.9.7
BuildRequires:	libicu-devel >= 4.8.1.1
# C++20
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	lua51-devel
BuildRequires:	luajit52-devel
BuildRequires:	meson >= 0.57.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	portaudio-devel >= 19
BuildRequires:	pulseaudio-devel >= 0.5
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	uchardet-devel
BuildRequires:	wxGTK3-unicode-devel >= 3.0.0
BuildRequires:	wxGTK3-unicode-gl-devel >= 3.0.0
BuildRequires:	wxWidgets-devel >= 3.0.0
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	ffms2 >= 2.22
Requires:	fftw3 >= 3.3
Requires:	fontconfig-libs >= 1:2.4
Requires:	hunspell >= 1.2.0
Requires:	libass >= 0.9.7
Requires:	libicu >= 4.8.1.1
Requires:	pulseaudio-libs >= 0.5
# due to luajit usage
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 mips mips64 mipsel ppc
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
%setup -q -n Aegisub-%{version}
%patch -P 0 -p1
%patch -P 2 -p1

cat >meson-native.ini <<EOF
[binaries]
wx-config = 'wx-gtk3-unicode-config'
EOF

%build
# avisynth,csri are Windows-specific in Aegisub (as of 3.4.2)
# directsound is Windows-only
%meson \
	--native-file meson-native.ini \
	-Dalsa=enabled \
	-Davisynth=disabled \
	-Dcsri=disabled \
	-Ddirectsound=disabled \
	-Denable_update_checker=false \
	-Dffms2=%{__enabled_disabled ffms2} \
	-Dfftw3=enabled \
	-Dhunspell=enabled \
	-Dopenal=enabled \
	-Dlibpulse=enabled \
	-Dportaudio=enabled \
	-Dsystem_luajit=true \
	-Duchardet=enabled

%if 0
# not required for dist tarballs
cat <<'EOF' >build/git_version.h
#define BUILD_GIT_VERSION_NUMBER 9426
#define BUILD_GIT_VERSION_STRING "%{version}"
#define TAGGED_RELEASE 1
#define INSTALLER_VERSION "%{version}"
#define RESOURCE_BASE_VERSION 3, 4, 2
EOF
%endif

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{fr_FR,fr}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{pt_PT,pt}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr_RS,sr}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr_RS,sr}@latin
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{uk_UA,uk}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc LICENCE README.md
%attr(755,root,root) %{_bindir}/aegisub
%{_datadir}/aegisub
%{_datadir}/metainfo/org.aegisub.Aegisub.metainfo.xml
%{_desktopdir}/org.aegisub.Aegisub.desktop
%{_iconsdir}/hicolor/*x*/apps/org.aegisub.Aegisub.png
%{_iconsdir}/hicolor/scalable/apps/org.aegisub.Aegisub.svg
