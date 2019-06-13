FROM codait/max-base:v1.1.1

ARG model_bucket=https://max-assets-dev.s3.us-south.cloud-object-storage.appdomain.cloud/max-nucleus-segmenter/1.0
ARG model_file=assets.tar.gz

# Add the missing packages for OpenCV
RUN apt-get update && apt-get install libgtk2.0 -y && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=assets/${model_file} && \
  tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace

RUN md5sum -c md5sums.txt # check file integrity

EXPOSE 5000

CMD python app.py
