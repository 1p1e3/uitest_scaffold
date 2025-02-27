# 暂时未经测试
FROM python:3.11
WORKDIR /uitest
COPY requirements.txt /uitest/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /uitest/
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-q"]



