#!/bin/sh
libtoolize --automake --copy --force
aclocal-1.9
autoheader
automake-1.9 --add-missing --force-missing --copy
autoconf
