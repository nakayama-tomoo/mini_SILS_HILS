FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    cmake \
    git \
    libgtest-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY . /workspace

RUN python3 -m pip install --break-system-packages -e ".[dev]"

RUN cmake -S cpp -B cpp/build

RUN cmake --build cpp/build

CMD bash -c "\
python3 -m pytest && \
python3 scripts/run_fan_control_sils.py && \
./cpp/build/run_scenario && \
python3 tools/compare_results.py"
