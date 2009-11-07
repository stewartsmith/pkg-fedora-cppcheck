Name:		cppcheck
Version:	1.38
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
for file in COPYING readme.txt; do
 iconv -f ASCII -t utf-8 $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

# Fix end of line encodings
for file in readme.txt; do
 sed -e 's|\r||g' $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

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
