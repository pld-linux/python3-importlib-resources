# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	importlib-resources
Summary:	Backport of Python standard library importlib.resources module for older Pythons
# Name must match the python module/package name (as on pypi or in 'import' statement)
Name:		python3-%{module}
Version:	6.5.2
Release:	1
License:	Apache v2
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/importlib-resources/
Source0:	https://files.pythonhosted.org/packages/source/i/importlib-resources/importlib_resources-%{version}.tar.gz
# Source0-md5:	6ba34e0f24dc7521a5e44e707ed0f28f
URL:		https://pypi.org/project/importlib-resources/
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-build
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-jaraco.test
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-tox
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Backport of Python standard library importlib.resources module for
older Pythons.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n importlib_resources-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" importlib_resources/tests
%endif

%if %{with doc}
%{_bindir}/tox -e docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS.rst README.rst
%dir %{py3_sitescriptdir}/importlib_resources
%{py3_sitescriptdir}/importlib_resources/*.py
%{py3_sitescriptdir}/importlib_resources/__pycache__
%{py3_sitescriptdir}/importlib_resources/py.typed
%dir %{py3_sitescriptdir}/importlib_resources/compat
%{py3_sitescriptdir}/importlib_resources/compat/*.py
%{py3_sitescriptdir}/importlib_resources/compat/__pycache__
%dir %{py3_sitescriptdir}/importlib_resources/future
%{py3_sitescriptdir}/importlib_resources/future/*.py
%{py3_sitescriptdir}/importlib_resources/future/__pycache__
%{py3_sitescriptdir}/importlib_resources-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
