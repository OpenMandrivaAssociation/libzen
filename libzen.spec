%define oname zen

%define major 0
%define libname	%mklibname %{oname} %{major}
%define devname %mklibname %{oname} -d

Summary:	Shared library for mediainfo
Name:		libzen
Version:		0.4.41
Release:		4
License:		BSD
Group:		System/Libraries
Url:		https://zenlib.sourceforge.net/
Source0:	https://mediaarea.net/download/source/%{name}/%{version}/%{name}_%{version}.tar.bz2
Patch0:		libzen-0.4.41-fix-build.patch
Patch1:		libzen-0.4.41-fix-pkgconfig-file-template.patch
BuildRequires:		cmake
BuildRequires:		dos2unix
BuildRequires:		doxygen
BuildRequires:		make

%description
Shared library for libmediainfo and mediainfo-gui.

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for mediainfo
Group:		System/Libraries

%description -n %{libname}
Shared library for libmediainfo and mediainfo-gui.

%files -n %{libname}
%doc *.txt
%{_libdir}/libzen.so.%{major}*

#-----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Include files and libraries for development
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	zenlib-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Include files and mandatory libraries for development with %{name}.

%files -n %{devname}
%doc Source/Doc/Documentation.html
%doc Doc/*
%dir %{_includedir}/ZenLib
%{_includedir}/ZenLib/*
%{_libdir}/libzen.so
%{_libdir}/cmake/zenlib/ZenLib*.cmake
%{_libdir}/pkgconfig/libzen.pc

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n ZenLib

# Fix EOLs and perms
dos2unix *.txt Source/Doc/*.html
chmod 644 *.txt Source/Doc/*.html


%build
pushd Project/CMake
	%cmake -DLIB_INSTALL_DIR="%{_libdir}"
	%make_build
popd

# Generate docs
pushd Source/Doc
        doxygen -u 2> /dev/null
        doxygen Doxyfile
popd


%install
pushd Project/CMake
	%make_install -C build
popd

# Fix pkgconfig file
#sed -i -e 's|libdir\=lib64 | libdir\=\/usr\/lib64|g' %%{buildroot}%%{_libdir}/pkgconfig/libzen.pc

%if 0
# Zenlib headers and ZenLib-config
install -dm 755 %{buildroot}%{_includedir}/ZenLib
install -m 644 Source/ZenLib/*.h %{buildroot}%{_includedir}/ZenLib

# Fix and install pkgconfig file
sed -i -e 's|Version: |Version: %{version}|g' Project/GNU/Library/libzen.pc
sed -i -e '/Libs_Static.*/d' Project/GNU/Library/libzen.pc

install -dm 755 %{buildroot}%{_libdir}/pkgconfig
install -m 644 Project/GNU/Library/libzen.pc %{buildroot}%{_libdir}/pkgconfig

# We don't want these
rm %{buildroot}%{_libdir}/libzen.la
%endif
