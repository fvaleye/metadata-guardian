***********
Development
***********

With Docker
===========
.. code-block:: bash

    # Inside the root folder
    docker build -t metadata_guardian ./

    # Build with Docker
    docker run -it metadata_guardian bash

With virtualenv
===============
.. code-block:: bash

    # Get virtualenv
    pip install virtualenv

    # Inside Python folder
    make setup-venv

    # Source
    source venv/bin/activate

    # Be ready to develop
    make develop

    # List everything
    make help