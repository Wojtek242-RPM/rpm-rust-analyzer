%global _hardened_build 1

%define git_release_tag 2020-11-16
%define pkg_release_tag %(echo %{git_release_tag} | sed -r "s/-//g")

# This file is encoded in UTF-8.  -*- coding: utf-8 -*-
Summary:       Implementation of the Language Server Protocol for the Rust programming language
Name:          rust-analyzer
Epoch:         1
Version:       0.0.0
Release:       0.1.%{pkg_release_tag}%{?dist}
License:       Apache-2.0 and MIT
URL:           https://rust-analyzer.github.io/
Source0:       https://github.com/rust-analyzer/rust-analyzer/archive/%{git_release_tag}.tar.gz#/%{name}-%{git_release_tag}.tar.gz
Patch1:        cargo-xtask-install.patch

BuildRequires: cargo
BuildRequires: rust

Provides:      %{name}(bin) = %{epoch}:%{version}-%{release}

%description
rust-analyzer is an implementation of the Language Server Protocol for the Rust
programming language. It provides features like completion and goto definition
for many code editors, including VS Code, Emacs and Vim.

Note that the project is in alpha status: it is already useful in practice, but
can't be considered stable.

%global debug_package %{nil}

%prep
%autosetup -n %{name}-%{git_release_tag} -p1

%build
%set_build_flags
cargo xtask dist

%install
cargo xtask install --server --srv-root %{buildroot}%{_prefix}

rm %{buildroot}%{_prefix}/.crates.toml
rm %{buildroot}%{_prefix}/.crates2.json

%files
%{_bindir}/%{name}

%changelog
* Sat Nov 21 2020 Wojciech Kozlowski <wk@wojciechkozlowski.eu>
- Initial spec file for alpha GitHub releases
