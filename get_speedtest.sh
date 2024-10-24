set -e

VERSION="1.2.0"
ARCH=$(uname -m)
curl -f -LO https://install.speedtest.net/app/cli/ookla-speedtest-$VERSION-linux-$ARCH.tgz
tar -xzf ookla-speedtest-$VERSION-linux-$ARCH.tgz speedtest
rm ookla-speedtest-$VERSION-linux-$ARCH.tgz