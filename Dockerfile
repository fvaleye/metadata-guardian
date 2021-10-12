FROM quay.io/pypa/manylinux2010_x86_64:2020-12-31-4928808

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
RUN $HOME/.cargo/bin/rustup default stable
ENV PATH /root/.cargo/bin:$PATH

# Setup Python
ENV PATH /opt/python/cp36-cp36m/bin:$PATH
RUN python -m pip install --upgrade pip

# Copy metadata guardian
COPY Cargo.toml metadata_guardian/Cargo.toml
COPY Cargo.lock metadata_guardian/Cargo.lock
COPY /rust metadata_guardian/rust
COPY /python metadata_guardian/python

WORKDIR metadata_guardian/python