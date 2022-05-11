FROM python:3.9.12
WORKDIR /scrapers
COPY . .
RUN pip install -r requirements.txt
RUN chmod a+x run.sh
ENTRYPOINT [ "./run.sh" ]