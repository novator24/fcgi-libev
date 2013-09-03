Name:           fcgi
Version:        2.4.0
Release:        10%{?dist}
Summary:        FastCGI development kit

Group:          Development/Languages
License:        BSD
URL:            http://www.fastcgi.com/#TheDevKit
Source0:        http://fastcgi.com/dist/fcgi-%{version}.tar.gz
Source1:        fcgi-autogen.sh
Patch0:         fcgi-2.4.0-autotools.patch
# Patch0 created with Source1 after patching Patch1 and Patch2
Patch1:         fcgi-2.4.0-configure.in.patch
Patch2:         fcgi-2.4.0-Makefile.am-CPPFLAGS.patch
Patch3:         fcgi-2.4.0-gcc44_fixes.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# for -perl
BuildRequires:  perl(ExtUtils::MakeMaker)

# don't "provide" private Perl libs
%global _use_internal_dependency_generator 0
%global provfind /bin/sh -c "grep -v '%perl_vendorarch.*\\.so$' | %__find_provides"
%global __find_provides %provfind

%description
FastCGI is a language independent, scalable, open extension to CGI that
provides high performance without the limitations of server specific APIs.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package perl
Summary:        Perl bindings for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description    perl
The %{name}-perl package contains the perl bindings for fcgi.


%prep
%setup -q
%patch0 -p1
%patch3 -p1 -b .gcc44_fixes

# remove DOS End Of Line Encoding
sed -i 's/\r//' doc/fastcgi-prog-guide/ch2c.htm
# fix file permissions
chmod a-x include/fcgios.h libfcgi/os_unix.c


%build
%configure
# does not build with parallel make flags
make

# build the perl bindings
cd perl
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/libfcgi{++,}.{l,}a
install -p -m 0644 -D doc/cgi-fcgi.1 $RPM_BUILD_ROOT%{_mandir}/man1/cgi-fcgi.1
for manpage in doc/*.3
do
install -p -m 0644 -D $manpage $RPM_BUILD_ROOT%{_mandir}/man3/$(basename $manpage)
done
rm -f -- doc/*.1
rm -f -- doc/*.3

# install the perl bindings
cd perl

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'

chmod -x *.fpl
%{_fixperms} $RPM_BUILD_ROOT/%{perl_vendorarch}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%check
# perl tests -- none presently, but that may change
cd perl && make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/cgi-fcgi
%{_libdir}/libfcgi.so.*
%{_libdir}/libfcgi++.so.*
%{_mandir}/man1/*
%defattr(0644,root,root,0755)
%doc LICENSE.TERMS README


%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libfcgi.so
%{_libdir}/libfcgi++.so
%{_mandir}/man3/*
%exclude %{_mandir}/man3/*.3pm*
%defattr(0644,root,root,0755)
%doc doc/


%files perl
%defattr(-,root,root,-)
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_mandir}/man3/*.3pm*
%defattr(0644,root,root,0755)
%doc perl/ChangeLog perl/README perl/*.fpl 


%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 01 2009 Chris Weyl <cweyl@alumni.drew.edu> - 2.4.0-9
- Stripping bad provides of private Perl extension libs

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Till Maas <opensource@till.name> - 2.4.0-7
- Add missing #include <cstdio> to make it compile with gcc 4.4

* Tue Oct 14 2008 Chris Weyl <cweyl@alumni.drew.edu> - 2.4.0-6
- package up the perl bindings in their own subpackage

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.4.0-5
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Till Maas <opensource till name> - 2.4.0-4
- bump release for rebuild

* Tue Jul 11 2007 Till Maas <opensource till name> - 2.4.0-3
- remove parallel make flags

* Tue Apr 17 2007 Till Maas <opensource till name> - 2.4.0-2
- add some documentation
- add mkdir ${RPM_BUILD_ROOT} to %%install
- install man-pages

* Mon Mar 5 2007 Till Maas <opensource till name> - 2.4.0-1
- Initial spec for fedora
