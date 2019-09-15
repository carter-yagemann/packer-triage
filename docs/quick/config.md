# Configuration

All configurations are kept in the `config` directory. All config files are
required and come with an example named `*.conf.example`. For this tutorial,
we'll use the defaults as-is, which will give us a sane setup for running
locally:

    cd config/
    cp frontend.conf.example frontend.conf
    cp database.conf.example database.conf
    # database.conf has passwords that must be changed
    sed -i "s/\"something_secret\"/\"$( dd if=/dev/urandom bs=1 count=32 | base64 )\"/" database.conf
    sed -i "s/\"another_secret\"/\"$( dd if=/dev/urandom bs=1 count=32 | base64 )\"/" database.conf
