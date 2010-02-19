### RPM external p5-poe 1.287
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn POE

Source: http://search.cpan.org/CPAN/authors/id/R/RC/RCAPUTO/%{downloadn}-%{realversion}.tar.gz

# Fake provides - these are all availalbe on a standard system but unknown to build system
Provides: perl(HTTP::Date)
Provides: perl(HTTP::Request)
Provides: perl(HTTP::Response)
Provides: perl(HTTP::Status)
Provides: perl(Term::ReadKey)
Provides: perl(URI)

# Lies - these are not actually provided by system perl
Provides: perl(Curses)
Provides: perl(Tk)

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL --default PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
