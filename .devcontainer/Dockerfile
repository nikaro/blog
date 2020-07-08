FROM nikaro/archlinux-dev

COPY requirements.txt .
RUN \
    # install required tools
    sudo pacman -Syu --noconfirm \
        jre-openjdk-headless \
        rsync \
        && \
    # pelican
    python3 -m pip install --user \
        -r requirements.txt \
        && \
    # clean up
    sudo rm -rf \
        /var/lib/pacman/sync \
        /var/cache/pacman/pkg \
        requirements.txt \
        &&  \
    :
