FROM ubuntu:18.04
RUN apt update -y && apt upgrade -y && apt install -y wget git build-essential
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda && conda create --name dev python=3.7.1 --channel conda-forge
RUN git clone https://github.com/sdorgancs/egpt.git
ENV PYTHONPATH=~/.egpt/plugins
RUN pip install egpt/
RUN cd egpt/plugins
RUN pip install plugins/egpt/nc_reader/ --target=$HOME/.egpt/plugins
RUN pip install plugins/egpt/test_task/ --target=$HOME/.egpt/plugins
RUN pip install plugins/egpt/test_wf/ --target=$HOME/.egpt/plugins