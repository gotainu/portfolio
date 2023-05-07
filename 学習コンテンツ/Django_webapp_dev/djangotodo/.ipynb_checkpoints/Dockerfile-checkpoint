FROM python:3
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
RUN pip install --upgrade setuptools
COPY . /code/

WORKDIR /opt

RUN apt-get update && apt-get install -y \
		wget \
		vim	

RUN wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh && \
		sh Anaconda3-2022.10-Linux-x86_64.sh -b -p /opt/anaconda3 && \
		rm -f Anaconda3-2022.10-Linux-x86_64.sh

ENV PATH /opt/anaconda3/bin:$PATH

RUN pip install --upgrade pip
WORKDIR /
CMD ["jupyter","lab","--ip=0.0.0.0","--allow-root","--LabApp.token="]