#!/usr/bin/env sh

SPEC_GIT_RELEASE=`grep "%define git_release_tag" rust-analyzer.spec | cut -d " " -f 3`
REMOTE_GIT_RELEASE=`git ls-remote --tags https://github.com/rust-analyzer/rust-analyzer.git | grep "refs/tags/20" | tail -n 1 | cut -d "/" -f 3`

if [ "${SPEC_GIT_RELEASE}" = "${REMOTE_GIT_RELEASE}" ]
then
    echo "No new git release : skipping update"
    exit 0
fi

echo "New git release {${REMOTE_GIT_RELEASE}} : updating"

PKGREL=`awk '/Release:/ {print $2}' rust-analyzer.spec | cut -d "." -f 2`
NEW_PKGREL=$((${PKGREL} + 1))

sed -i "s/git_release_tag ${SPEC_GIT_RELEASE}/git_release_tag ${REMOTE_GIT_RELEASE}/" rust-analyzer.spec
sed -ri "s/(Release:\s+0.)[0-9]+/\1${NEW_PKGREL}/" rust-analyzer.spec
