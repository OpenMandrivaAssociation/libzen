%define oname zen

%define major 0
%define libname	%mklibname %{oname} %{major}
%define devname %mklibname %{oname} -d

Name:		libzen
Version:	0.4.37
Release:	2
Summary:	Shared library for mediainfo
Group:		System/Libraries
License:	BSD
URL:		http://zenlib.sourceforge.net/
Source0:	http://mediaarea.net/download/source/%{name}/%{version}/%{name}_%{version}.tar.bz2
Patch0:		libzen_0.4.20-fix-build.patch
BuildRequires:	dos2unix
BuildRequires:	doxygen

%description
Shared library for libmediainfo and mediainfo-gui.

%package -n %{libname}
Summary:	Shared library for mediainfo
Group:		System/Libraries

%description -n %{libname}
Shared library for libmediainfo and mediainfo-gui.

%package -n %{devname}
Summary:	Include files and libraries for development
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	zenlib-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Include files and mandatory libraries for development.

%prep
%setup -q -n ZenLib
%patch0 -p0

#fix EOLs and rights
dos2unix *.txt Source/Doc/*.html
chmod 644 *.txt Source/Doc/*.html

%build
pushd Project/GNU/Library
	autoreconf -vfi
	%configure2_5x \
		--enable-shared \
		--disable-static
	%make
popd

# generate docs
pushd Source/Doc
        doxygen -u 2> /dev/null
        doxygen Doxyfile
popd

%install
pushd Project/GNU/Library
	%makeinstall_std
popd

# Zenlib headers and ZenLib-config
install -dm 755 %{buildroot}%{_includedir}/ZenLib
install -m 644 Source/ZenLib/*.h %{buildroot}%{_includedir}/ZenLib

#fix and install pkgconfig file
sed -i -e 's|Version: |Version: %{version}|g' Project/GNU/Library/libzen.pc
sed -i -e '/Libs_Static.*/d' Project/GNU/Library/libzen.pc

install -dm 755 %{buildroot}%{_libdir}/pkgconfig
install -m 644 Project/GNU/Library/libzen.pc %{buildroot}%{_libdir}/pkgconfig

#we don't want these
rm %{buildroot}%{_libdir}/libzen.la

%files -n %{libname}
%doc *.txt
%{_libdir}/libzen.so.%{major}*

%files -n %{devname}
%doc Source/Doc/Documentation.html
%doc Doc/*
%{_includedir}/ZenLib
# Disable, file is removed from upstream
#{_bindir}/libzen-config
%{_libdir}/libzen.so
%{_libdir}/pkgconfig/*.pc
