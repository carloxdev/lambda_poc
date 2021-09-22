FROM python:3.8-buster

# RUN groupadd app && useradd -g app -m app
# RUN mkdir /app && chown app:app /app
# RUN export PATH="/home/app/.local/bin:$PATH" >> /home/app/.bashrc
# RUN source /home/app/.bashrc
# RUN echo $PATH
# USER app

WORKDIR /app
COPY requirements.txt ./

# RUN apt install build-essential
RUN pip install -r requirements.txt
RUN pip install pytest coverage

COPY . .

RUN chmod +x docker-entrypoint.sh

CMD ["coverage", "run", "--source=.", "-m", "unittest", "--v", "test/test_child_app.py"]
#  coverage run --source=. -m unittest --v test/test_office_app.py
