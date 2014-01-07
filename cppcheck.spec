Name:		cppcheck
Version:	1.63
Release:	1%{?dist}
Summary:	Tool for static C/C++ code analysis
Group:		Development/Languages
License:	GPLv3+
URL:		http://cppcheck.wiki.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	pcre-devel
BuildRequires:	tinyxml2-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt

%description
Cppcheck is a static analysis tool for C/C++ code. Unlike C/C++
compilers and many other analysis tools it does not detect syntax
errors in the code. Cppcheck primarily detects the types of bugs that
the compilers normally do not detect. The goal is to detect only real
errors in the code (i.e. have zero false positives).


%prep
%setup -q
# Make sure bundled tinyxml is not used
rm -r externals/tinyxml

%build
# TINYXML= prevents use of bundled tinyxml
CXXFLAGS="%{optflags} -DNDEBUG $(pcre-config --cflags)" \
    LDFLAGS="$RPM_LD_FLAGS" LIBS=-ltinyxml2 make TINYXML= \
    DB2MAN=%{_datadir}/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl \
    %{?_smp_mflags} all man
xsltproc --nonet -o man/manual.html \
    %{_datadir}/sgml/docbook/xsl-stylesheets/xhtml/docbook.xsl \
    man/manual.docbook

%install
rm -rf %{buildroot}
install -D -p -m 755 cppcheck %{buildroot}%{_bindir}/cppcheck
install -D -p -m 644 cppcheck.1 %{buildroot}%{_mandir}/man1/cppcheck.1

%check
make TINYXML= check

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING man/manual.html
%{_bindir}/cppcheck
%{_mandir}/man1/cppcheck.1*

%changelog
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
