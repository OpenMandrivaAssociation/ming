%define major 1
%define libname %mklibname ming %{major}
%define develname %mklibname ming -d

Summary:	Ming - an SWF output library
Name:		ming
Version:	0.4.3
Release:	%mkrel 8
License:	LGPL
Group:		System/Libraries
URL:		http://www.libming.org/
Source0:	http://prdownloads.sourceforge.net/ming/%{name}-%{version}.tar.bz2
Patch0:		ming-0.4.3-fix-linkage.patch
Patch1:		05_shared_perl
Patch2:		07-GvCV-isn-t-an-lvalue-since-Perl-5.13.10.patch
Patch3:		08_libpng15.patch
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	flex
BuildRequires:	freetype2-devel
BuildRequires:	jpeg-devel
BuildRequires:	perl-devel
BuildRequires:	png-devel
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	giflib-devel
BuildRequires:	zlib-devel
BuildRequires:	libx11-devel
BuildRequires:	pkgconfig
# gotta conflict here, otherwise stuff will be linked against installed libs...
BuildConflicts:	ming-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Ming is a c library for generating SWF ("Flash") format movies. This 
package only contains the basic c-based library.

%package -n	%{libname}
Summary:	Ming - an SWF output library
Group:		System/Libraries

%description -n	%{libname}
Ming is a c library for generating SWF ("Flash") format movies.
This package only contains the basic c-based library.

%package -n	%{develname}
Summary:	Ming development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}
Obsoletes:	%{libname}-devel = %{version}

%description -n	%{develname}
The %{name}-devel package contains the header files
and static libraries necessary for developing programs using the
%{name}-devel library (C and C++)..

%package -n	perl-SWF
Summary:	Ming perl module
Group:		Development/Perl
Provides:       perl-ming
Obsoletes:      perl-ming
Requires:	%{libname} = %{version}-%{release}

%description -n	perl-SWF
Ming perl module - perl wrapper for the Ming library.

%package -n	python-SWF
Summary:	Ming python module
Group:		Development/Python
Requires:	%{libname} = %{version}-%{release}

%description -n	python-SWF
Python module - python wrapper for the Ming library.

%package -n	%{name}-utils
Summary:	Ming utilities
Group:		File tools
Requires:	%{libname} = %{version}-%{release}

%description -n %{name}-utils
This package contains various ming utilities.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

# fix attribs
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

# cleanup
for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# fix python
perl -pi -e "s|/usr/local/include\b|%{_includedir}|g;s|/usr/local/lib\b|%{_libdir}|g" py_ext/setup.py

%build
autoreconf -fi
%configure2_5x \
    --enable-shared \
    --disable-static

%make

pushd perl_ext
    perl Makefile.PL LIBS="-L%{_libdir} -ljpeg `pkg-config --libs libpng` -lz -lm -lgif" INSTALLDIRS=vendor </dev/null
    make
#    make test
popd

pushd py_ext
    env CFLAGS="%{optflags}" python setup.py build
popd

%install
rm -rf %{buildroot}

%makeinstall_std

# install the perl extension
%makeinstall_std -C perl_ext

# install the python extension
pushd py_ext
    python setup.py install --root=%{buildroot}
popd

# fix docs
cp perl_ext/README perl_ext.README
cp util/README util.README
chmod 644 ChangeLog HISTORY INSTALL *README* TODO

# cleanup
rm -rf %{buildroot}%{perl_vendorlib}/*/auto/SWF/include
rm -rf %{buildroot}%{_libdir}/libming.*a

# nuke rpath
find %{buildroot}%{perl_vendorlib} -name "*.so" | xargs chrpath -d

chmod 755 %{buildroot}%{_bindir}/ming-config

%multiarch_binaries %{buildroot}%{_bindir}/ming-config

# install man pages
install -d %{buildroot}%{_mandir}/man1
install -m0644 docs/man/*.1 %{buildroot}%{_mandir}/man1/

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc ChangeLog HISTORY README TODO
%attr(0755,root,root) %{_libdir}/libming.so.%{major}*

%files -n %{develname}
%defattr(644,root,root,755)
%attr(755,root,root) %{multiarch_bindir}/ming-config
%attr(0755,root,root) %{_bindir}/ming-config
%attr(0755,root,root) %{_libdir}/libming.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libming.pc
%{_includedir}/*

%files -n perl-SWF
%defattr(-,root,root)
%doc perl_ext.README perl_ext/examples
%dir %{perl_vendorlib}/*/auto/SWF
%dir %{perl_vendorlib}/*/SWF
%{perl_vendorlib}/*/auto/SWF/SWF.so
%{perl_vendorlib}/*/*.pm
%{perl_vendorlib}/*/SWF/*.pm
%{_mandir}/man3*/SWF*

%files -n python-SWF
%defattr(-,root,root)
%doc py_ext/README
%{py_platsitedir}/*.so
%{py_platsitedir}/*.py*
%{py_platsitedir}/*.egg-info

%files -n %{name}-utils
%defattr(644,root,root,755)
%doc util.README
%attr(755,root,root) %{_bindir}/dbl2png
%attr(755,root,root) %{_bindir}/gif2dbl
%attr(755,root,root) %{_bindir}/gif2mask
%attr(755,root,root) %{_bindir}/listaction
%attr(755,root,root) %{_bindir}/listaction_d
%attr(755,root,root) %{_bindir}/listfdb
%attr(755,root,root) %{_bindir}/listjpeg
%attr(755,root,root) %{_bindir}/listmp3
%attr(755,root,root) %{_bindir}/listswf
%attr(755,root,root) %{_bindir}/listswf_d
%attr(755,root,root) %{_bindir}/makefdb
%attr(755,root,root) %{_bindir}/makeswf
%attr(755,root,root) %{_bindir}/png2dbl
%attr(755,root,root) %{_bindir}/raw2adpcm
%attr(755,root,root) %{_bindir}/swftocxx
%attr(755,root,root) %{_bindir}/swftoperl
%attr(755,root,root) %{_bindir}/swftophp
%attr(755,root,root) %{_bindir}/swftopython
%attr(755,root,root) %{_bindir}/swftotcl
%{_mandir}/man1/dbl2png.1*
%{_mandir}/man1/gif2dbl.1*
%{_mandir}/man1/gif2mask.1*
%{_mandir}/man1/listfdb.1*
%{_mandir}/man1/listjpeg.1*
%{_mandir}/man1/listmp3.1*
%{_mandir}/man1/makefdb.1*
%{_mandir}/man1/makeswf.1*
%{_mandir}/man1/png2dbl.1*
%{_mandir}/man1/raw2adpcm.1*
%{_mandir}/man1/swftocxx.1*
%{_mandir}/man1/swftoperl.1*
%{_mandir}/man1/swftophp.1*
%{_mandir}/man1/swftopython.1*
%{_mandir}/man1/swftotcl.1*
