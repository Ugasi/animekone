FROM python:3.11.6-alpine3.18
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x ./get_salkkarit.py
RUN mkdir /downloads
RUN crontab 0 15 * * 5 python ./get_salkkarit.py >> /logfile
CMD ["crond", "-f"]