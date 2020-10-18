# why
    to build a personal blog
# how
    build a swift server base on flask
# what
    a swift blog server

# cmds
    cd apps
    mkvirtualenv blog -p python3
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    or
    cd apps
    sh setup.sh
  
# route
    /     # welcome
    /books    # book list
    /books/<path:filename>    # html book get
    /static/<path:filename>    # static file get
    