FROM nikaro/alpine-dev

RUN \
    sudo apk add \
        go \
        hugo \
        && \
    cd /tmp && \
    git clone https://git.sr.ht/~sircmpwn/openring && \
    cd openring/ && \
    go build -o $HOME/.local/bin/openring && \
    :
