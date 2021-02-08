FROM ggutierrezbio/ambertools20 as mdmix3
RUN python3 -m pip install --upgrade pip setuptools
WORKDIR /mdmix3
ADD pymdmix ./pymdmix
ADD requirements.txt ./requirements.txt
ADD src ./src
ADD setup.py ./setup.py
RUN python3 -m pip install .

FROM mdmix3 as mdmix3-test
ADD ./dev-requirements.txt ./dev-requirements.txt
RUN python3 -m pip install -r dev-requirements.txt
ADD ./tests ./tests