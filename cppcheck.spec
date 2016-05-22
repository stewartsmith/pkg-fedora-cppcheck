Name:		cppcheck
Version:	1.73
Release:	2%{?dist}
Summary:	Tool for static C/C++ code analysis
Group:		Development/Languages
License:	GPLv3+
URL:		http://cppcheck.wiki.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:        cppcheck.desktop
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Use system tinyxml2
Patch0:         cppcheck-1.73-tinyxml.patch
# Fix location of translations
Patch1:         cppcheck-1.73-translations.patch

BuildRequires:	pcre-devel
BuildRequires:	tinyxml2-devel >= 2.1.0
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt
BuildRequires:  qt4-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils

%description
Cppcheck is a static analysis tool for C/C++ code. Unlike C/C++
compilers and many other analysis tools it does not detect syntax
errors in the code. Cppcheck primarily detects the types of bugs that
the compilers normally do not detect. The goal is to detect only real
errors in the code (i.e. have zero false positives).

%package gui
Summary:        Graphical user interface for cppcheck
Group:          Applications/Engineering
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gui
This package contains the graphical user interface for cppcheck.


%prep
%setup -q
%patch0 -p1 -b .tinyxml
%patch1 -p1 -b .translations
# Make sure bundled tinyxml is not used
rm -r externals/tinyxml

%build
# Manuals
make DB2MAN=%{_datadir}/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl man 
xsltproc --nonet -o man/manual.html \
    %{_datadir}/sgml/docbook/xsl-stylesheets/xhtml/docbook.xsl \
    man/manual.docbook

# Binaries
mkdir objdir-%{_target_platform}
cd objdir-%{_target_platform}
# Upstream doesn't support shared libraries (unversioned solib)
%cmake .. -DCMAKE_BUILD_TYPE=Release -DHAVE_RULES=1 -DBUILD_GUI=1 -DBUILD_SHARED_LIBS:BOOL=OFF -DBUILD_TESTS=1
# SMP make doesn't seem to work
make cppcheck

%install
rm -rf %{buildroot}
make -C objdir-%{_target_platform} DESTDIR=%{buildroot} install
install -D -p -m 644 cppcheck.1 %{buildroot}%{_mandir}/man1/cppcheck.1

# Install desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
# Install logo
install -D -p -m 644 gui/icon.png %{buildroot}%{_datadir}/pixmaps/cppcheck.png

%check
cd objdir-%{_target_platform}/bin
# A test currently fails on 32-bit archs, see http://trac.cppcheck.net/ticket/7037
%if 0%{?__isa_bits} == 64
./testrunner -g -q
%endif

%clean
rm -rf %{buildroot}

%files
%doc AUTHORS COPYING man/manual.html
%{_datadir}/CppCheck/
%{_bindir}/cppcheck
%{_mandir}/man1/cppcheck.1*

%files gui
%{_bindir}/cppcheck-gui
%{_datadir}/applications/cppcheck.desktop
%{_datadir}/pixmaps/cppcheck.png


%changelog
* Sun May 22 2016 Rich Mattes <richmattes@gmail.com> - 1.73-2
- Rebuild for tinyxml2-3.0.0

* Sat Apr 09 2016 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.73-1
- Update to 1.73.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 14 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.71-1
- Update to 1.71.

* Fri Nov 13 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.70-4
- Link whole archive (BZ #1280242), patch by Mamoru Tasaka.
- Compile and run tests using CMake.

* Wed Nov 11 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.70-3
- Enable HAVE_RULES.

* Thu Nov 5 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.70-2
- Include GUI (BZ #1278318).

* Mon Sep 21 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.70-1
- Update to 1.70.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.68-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Jan 03 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.68-1
- Update to 1.68.

* Mon Dec 01 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.67-1
- Update to 1.67.

* Sat Aug 23 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.66-1
- Update to 1.66.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.65-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.65-1
- Update to 1.65.

* Wed Jan 22 2014 François Cami <fcami@fedoraproject.org> - 1.63-3
- Add HAVE_RULES=yes (#1056733).

* Tue Jan 07 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.63-2
- Include cfg files as well.

* Tue Jan 07 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.63-1
- Update to 1.63.

* Sun Oct 13 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.62-1
- Update to 1.62.

* Sat Aug 10 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.61-1
- Update to 1.61.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.60.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 François Cami <fcami@fedoraproject.org> - 1.60.1-1
- Update to 1.60.1.

* Mon Apr 01 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.59-1
- Update to 1.59.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 François Cami <fcami@fedoraproject.org> - 1.58-1
- Update to 1.58.

* Tue Sep 18 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.57-1
- Update to 1.57.

* Tue Sep 18 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.56-1
- Update to 1.56.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.55-1
- Update to 1.55.

* Sun Apr 15 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.54-1
- Update to 1.54.

* Sat Feb 11 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.53-1
- Update to 1.53.

* Thu Jan 05 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.52-2
- Add missing includes (fix FTBFS in rawhide).

* Sun Dec 11 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.52-1
- Update to 1.52.

* Wed Oct 26 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.51-2
- Include man page and more other docs.
- Build with $RPM_LD_FLAGS.
- Improve summary and description.

* Sun Oct 09 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.51-1
- Update to 1.51.

* Fri Aug 19 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.50-2
- Fix build on EPEL-4.

* Sun Aug 14 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.50-1
- Update to 1.50.

* Mon Jun 13 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.49-1
- Update to 1.49.

* Sat Apr 30 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.48-2
- Build with system tinyxml and support for rules.
- Run test suite during build, don't include its sources in docs.
- Drop readme.txt from docs, it doesn't contain useful info after installed.

* Fri Apr 15 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.48-1
- Update to 1.48.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.47-1
- Update to 1.47.

* Thu Dec 30 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.46.1-1
- Update to 1.46.1.

* Wed Dec 15 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.46-1
- Update to 1.46.

* Mon Oct 4 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.45-1
- Update to 1.45.

* Sat Jul 24 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.44-1
- Update to 1.44.

* Sun May 9 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.43-1
- Update to 1.43.

* Wed Mar 10 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.42-1
- Update to 1.42.

* Mon Jan 18 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.40-1
- Update to 1.40.

* Sun Dec 27 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.39-1
- Update to 1.39.

* Sat Nov 07 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.38-1
- Update to 1.38.

* Tue Sep 22 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.36-1
- Update to 1.36.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.34-1
- Update to 1.34.

* Mon Apr 27 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.31-1
- First release.
