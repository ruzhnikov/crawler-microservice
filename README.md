# NAME

Exness crawler microservice

## DESCRIPTION

Test exercise. Service for obtaining data

## INSTALL

```
    virtualenv --python=python3 env
    source ./env/bin/activate
    pip install Flask
    cd <path of exness-crawler>
    python setup.py install
    cd <path of this app>
    python app.py
```
## USING

Open in your browser a link http://localhost:5000/api/1.0/rss?url=&lt;url&gt;&count=&lt;count&gt;  
Where
* &lt;url&gt; -- Mandatory argument. A whole address of RSS resource, for example https://habr.com/rss/best/
* &lt;count&gt; -- Optional argument. A count of records that you want to get. By default, unlimited

The response of server will be containt JSON with crabbed data
