%define major 1
%define libname %mklibname ming %{major}
%define devname %mklibname ming -d

Summary:	Ming - an SWF output library
Name:		ming
Version:	0.4.5
Release:	4
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.libming.org/
Source0:	http://prdownloads.sourceforge.net/ming/%{name}-%{version}.tar.bz2
Patch0:		ming-automake-1.13.patch
Patch1:		ming-0.4.5-giflib51.patch
BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	jpeg-devel
BuildRequires:	giflib-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
# gotta conflict here, otherwise stuff will be linked against installed libs...
BuildConflicts:	ming-devel

%description
Ming is a c library for generating SWF ("Flash") format movies. This 
package only contains the basic c-based library.

%package -n	%{libname}
Summary:	Ming - an SWF output library
Group:		System/Libraries

%description -n	%{libname}
Ming is a c library for generating SWF ("Flash") format movies.
This package only contains the basic c-based library.

%package -n	%{devname}
Summary:	Ming development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development files for %{name}.

%package -n	perl-SWF
Summary:	Ming perl module
Group:		Development/Perl
Provides:	perl-ming = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	perl-SWF
Ming perl module - perl wrapper for the Ming library.

%package -n	python-SWF
Summary:	Ming python module
Group:		Development/Python

%description -n	python-SWF
Python module - python wrapper for the Ming library.

%package -n	%{name}-utils
Summary:	Ming utilities
Group:		File tools

%description -n %{name}-utils
This package contains various ming utilities.

%prep
%setup -q
%apply_patches

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
autoreconf -fi

%build
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
chmod 644 NEWS HISTORY INSTALL *README* TODO

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

%files -n %{libname}
%{_libdir}/libming.so.%{major}*

%files -n %{devname}
%doc NEWS HISTORY README TODO
%{multiarch_bindir}/ming-config
%{_bindir}/ming-config
%{_libdir}/libming.so
%{_libdir}/pkgconfig/libming.pc
%{_includedir}/*

%files -n perl-SWF
%doc perl_ext.README perl_ext/examples
%dir %{perl_vendorlib}/*/auto/SWF
%dir %{perl_vendorlib}/*/SWF
%{perl_vendorlib}/*/auto/SWF/SWF.so
%{perl_vendorlib}/*/*.pm
%{perl_vendorlib}/*/SWF/*.pm
%{_mandir}/man3*/SWF*

%files -n python-SWF
%doc py_ext/README
%{py_platsitedir}/*.so
%{py_platsitedir}/*.py*
%{py_platsitedir}/*.egg-info

%files -n %{name}-utils
%doc util.README
%{_bindir}/dbl2png
%{_bindir}/gif2dbl
%{_bindir}/gif2mask
%{_bindir}/listaction
%{_bindir}/listaction_d
%{_bindir}/listfdb
%{_bindir}/listjpeg
%{_bindir}/listmp3
%{_bindir}/listswf
%{_bindir}/listswf_d
%{_bindir}/makefdb
%{_bindir}/makeswf
%{_bindir}/png2dbl
%{_bindir}/raw2adpcm
%{_bindir}/swftocxx
%{_bindir}/swftoperl
%{_bindir}/swftophp
%{_bindir}/swftopython
%{_bindir}/swftotcl
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

