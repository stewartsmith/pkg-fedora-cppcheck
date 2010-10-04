Name:		cppcheck
Version:	1.45
Release:	1%{?dist}
Summary:	A tool for static C/C++ code analysis
Group:		Development/Languages
License:	GPLv3+
URL:		http://cppcheck.wiki.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
This program tries to detect bugs that your C/C++ compiler don't see.
The goal is no false positives.

Your compiler can detect many problems that cppcheck don't try to detect.
We recommend that you enable as many warnings as possible in your compiler.

Cppcheck is versatile. You can check non-standard code that includes
various compiler extensions, inline assembly code, etc.


%prep
%setup -q
# Convert text files to UTF-8
for file in COPYING readme.txt test/tinyxml/tinystr.cpp test/tinyxml/changes.txt; do
 iconv -f ISO-8859-15 -t utf-8 $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

# Fix end of line encodings
for file in readme.txt test/test.vcproj test/test.vcxproj{,.filters}; do
 sed -e 's|\r||g' $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

# Fix permissions
find -name "*.cpp" -exec chmod 644 {} \;
find -name "*.vcproj" -exec chmod 644 {} \;

%build
make CXXFLAGS="%{optflags}" %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -D -p -m 755 cppcheck %{buildroot}%{_bindir}/cppcheck

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING readme.txt test/
%{_bindir}/cppcheck

%changelog
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
