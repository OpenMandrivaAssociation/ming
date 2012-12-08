%define major 1
%define libname %mklibname ming %{major}
%define develname %mklibname ming -d

Summary:	Ming - an SWF output library
Name:		ming
Version:	0.4.4
Release:	1
License:	LGPL
Group:		System/Libraries
URL:		http://www.libming.org/
Source0:	http://prdownloads.sourceforge.net/ming/%{name}-%{version}.tar.bz2
Patch1:		05_shared_perl
Patch2:		07-GvCV-isn-t-an-lvalue-since-Perl-5.13.10.patch
Patch3:		ming-0.4.4-vasprintf.patch
BuildRequires:	autoconf automake libtool
BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	flex
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	jpeg-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	giflib-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(x11)
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

%package -n	%{develname}
Summary:	Ming development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
The %{name}-devel package contains the header files
and static libraries necessary for developing programs using the
%{name}-devel library (C and C++)..

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
%setup -q
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
%doc NEWS HISTORY README TODO
%attr(0755,root,root) %{_libdir}/libming.so.%{major}*

%files -n %{develname}
%attr(755,root,root) %{multiarch_bindir}/ming-config
%attr(0755,root,root) %{_bindir}/ming-config
%attr(0755,root,root) %{_libdir}/libming.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libming.pc
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


%changelog
* Sun Mar 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.4.4-1
+ Revision: 784202
- 0.4.4
- drop redundant patches
- various fixes

* Sun Jan 22 2012 Oden Eriksson <oeriksson@mandriva.com> 0.4.3-9
+ Revision: 765937
- rebuilt for perl-5.14.2

* Tue Oct 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.3-8
+ Revision: 702665
- sync patches with debian, etc
- fix friggin deps again
- attempt to relink against libpng15.so.15

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.3-7
+ Revision: 661703
- multiarch fixes

* Mon Mar 21 2011 Funda Wang <fwang@mandriva.org> 0.4.3-6
+ Revision: 647248
- rebuild
- cleanup spec file

* Tue Nov 02 2010 Funda Wang <fwang@mandriva.org> 0.4.3-4mdv2011.0
+ Revision: 592110
- rebuild for py2.7

* Sun Aug 01 2010 Funda Wang <fwang@mandriva.org> 0.4.3-3mdv2011.0
+ Revision: 564308
- rebuild for perl 5.12.1

* Thu Jul 22 2010 Jérôme Quelin <jquelin@mandriva.org> 0.4.3-2mdv2011.0
+ Revision: 556780
- perl 5.12 rebuild

* Mon Feb 08 2010 Emmanuel Andry <eandry@mandriva.org> 0.4.3-1mdv2010.1
+ Revision: 502214
- fix BR
- New version 0.4.3
- rediff p0
- drop p3 (now useless)
- update files list

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-7mdv2010.1
+ Revision: 488787
- rebuilt against libjpeg v8

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-6mdv2010.0
+ Revision: 416661
- rebuilt against libjpeg v7

* Sat Dec 27 2008 Funda Wang <fwang@mandriva.org> 0.4.2-5mdv2009.1
+ Revision: 319826
- fix str fmt
- rebuild for new python

* Fri Nov 21 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-3mdv2009.1
+ Revision: 305486
- really make it backportable...

* Fri Nov 21 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-2mdv2009.1
+ Revision: 305468
- make it backportable

* Thu Sep 25 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-1mdv2009.0
+ Revision: 288076
- 0.4.2
- rediffed P0
- dropped redundant patches

* Mon Aug 25 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-0.rc1.1mdv2009.0
+ Revision: 275712
- 0.4.0.rc1
- drop implemented and obsolete patches
- fix linkage (P0)
- rediffed two patches
- drop the perl and python sources, it's bundled now

* Sat Aug 23 2008 Emmanuel Andry <eandry@mandriva.org> 0.3.0-10mdv2009.0
+ Revision: 275267
- apply devel policy
- drop old conditionnal
- check major

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0.3.0-9mdv2009.0
+ Revision: 265127
- rebuild early 2009.0 package (before pixel changes)

* Wed Jun 11 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-8mdv2009.0
+ Revision: 218120
- fix build

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Jan 16 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-7mdv2008.1
+ Revision: 153649
- added P5 from PLD to make it link against the shared lib
- added some spec file fixes

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rebuild for perl-5.10.0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.0-5mdv2008.0
+ Revision: 89931
- rebuild


* Wed Jan 31 2007 Nicolas Lécureuil <neoclust@mandriva.org> 0.3.0-4mdv2007.0
+ Revision: 115787
- Fix Buildrequires (thanks iurt)
- Rebuild against new python
- Import ming

* Wed Jul 26 2006 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-1mdv2007.0
- 0.3.0

* Tue May 23 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.3.0-0.beta2.7mdk
- fix requires

* Sat May 20 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.3.0-0.beta2.6mdk
- fix buildrequires

* Tue Feb 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-0.beta2.5mdk
- rebuild

* Tue Feb 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-0.beta2.4mdk
- fix multiarch compliance

* Tue Feb 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-0.beta2.3mdk
- fix one minor glitch in the spec file

* Tue Feb 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-0.beta2.2mdk
- the code is too borked to be unbundled...

* Wed Nov 02 2005 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-0.beta2.1mdk
- 0.3.0 beta2
- drop upstream patches; P0
- rediffed P2,P3
- fix sane microversion (P4)
- fix deps
- the perl and python sub packages has been broken out

* Wed Nov 02 2005 Oden Eriksson <oeriksson@mandriva.com> 0.3-1.20050815.1mdk
- new snap (20050815)
- rediffed P0 (different approach)
- rediffed P1 (gcc4)
- added P2 (DESTDIR)
- added the python sub package, fixes #18919
- added P3 to pass -fPIC to the compiler cflags when building the lib

* Wed Nov 02 2005 Oden Eriksson <oeriksson@mandriva.com> 0.3-0.beta1.9mdk
- added one gcc4 patch

* Fri Dec 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.3-0.beta1.8mdk
- revert latest "lib64 fixes"

* Tue Dec 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.3-0.beta1.7mdk
- lib64 fixes
- nuke rpath

* Fri Dec 10 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.3-0.beta1.6mdk
- added an obvious lib64 fix

* Thu Dec 02 2004 Abel Cheung <deaddog@mandrake.org> 0.3-0.beta1.5mdk
- And another...

* Thu Dec 02 2004 Abel Cheung <deaddog@mandrake.org> 0.3-0.beta1.4mdk
- Fix BuildRequires

* Mon Nov 15 2004 Michael Scherer <misc@mandrake.org> 0.3-0.beta1.3mdk
- Rebuild for new perl
- Rename the perl module to perl-SWF, more compliant with the naming policy

* Tue May 25 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.beta1.2mdk
- misc spec file fixes
- drop P2, use spec file hack instead
- fix deps

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.beta1.1mdk
- 0.3beta1
- new url
- misc spec file fixes

