%global _hardened_build 1

%define git_release_tag 2022-09-12
%define pkg_release_tag %(echo %{git_release_tag} | sed -r "s/-//g")

# This file is encoded in UTF-8.  -*- coding: utf-8 -*-
Summary:       Implementation of the Language Server Protocol for the Rust programming language
Name:          rust-analyzer
Epoch:         1
Version:       0.0.0
Release:       0.98.%{pkg_release_tag}%{?dist}
License:       ASL 2.0 and MIT
URL:           https://rust-analyzer.github.io/
Source0:       https://github.com/rust-analyzer/rust-analyzer/archive/%{git_release_tag}.tar.gz
# For some reason rpkg packs the current directory as the source tarball if there is nothing else
# other than Source0.
Source1:       check-and-update.sh

ExclusiveArch:  %{rust_arches}

BuildRequires: rust-packaging

Provides:      %{name}(bin) = %{epoch}:%{version}-%{release}

%description
rust-analyzer is an implementation of the Language Server Protocol for the Rust
programming language. It provides features like completion and goto definition
for many code editors, including VS Code, Emacs and Vim.

Note that the project is in alpha status: it is already useful in practice, but
can't be considered stable.

%prep
%autosetup -n %{name}-%{git_release_tag} -p1
# use bits of rust-packaging magic without local registry definition
mkdir -p .cargo
cat > .cargo/config << EOF
[build]
rustc = "%{__rustc}"
rustdoc = "%{__rustdoc}"
rustflags = %{__global_rustflags_toml}

[install]
root = "%{buildroot}%{_prefix}"

[term]
verbose = true
EOF

%build
%{__cargo} build %{__cargo_common_opts} --release --manifest-path ./crates/rust-analyzer/Cargo.toml --bin rust-analyzer

%install
%{__cargo} install %{__cargo_common_opts} --locked --no-track --path crates/%{name}

%files
%license LICENSE-APACHE LICENSE-MIT
%doc PRIVACY.md README.md docs/user/*
%{_bindir}/%{name}

%changelog
* Sun Nov 22 2020 Wojciech Kozlowski <wk@wojciechkozlowski.eu>
- Use rpmbuild macros for cargo
- Align with typical Fedora packaging
- Remove cargo-xtask-install.patch

* Sat Nov 21 2020 Wojciech Kozlowski <wk@wojciechkozlowski.eu>
- Initial spec file for alpha GitHub releases
