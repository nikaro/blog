FROM nikaro/debian-dev

COPY requirements.txt .
RUN \
    # install required tools
    sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends \
        openjdk-11-jre-headless \
        python3-pip \
        rsync \
        && \
    # pelican
    python3 -m pip install --user --upgrade \
        pip \
        setuptools \
        wheel \
        && \
    python3 -m pip install --user \
        -r requirements.txt \
        && \
    # clean up
    sudo apt-get clean && \
    sudo rm -rf \
        /var/cache/apt/ \
        /var/lib/apt/lists/* \
        requirements.txt \
        && \
    :
