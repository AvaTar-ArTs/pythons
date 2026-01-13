Quick Start Guide
=================

Get started with the Python Automation Arsenal in minutes!

Prerequisites
-------------

Required:
   - Python 3.8 or higher
   - Mamba/Conda environment manager
   - Git

Optional but recommended:
   - API keys for AI services (already configured in ``~/.env.d/``)
   - 26+ AI/ML service accounts

Installation
------------

1. **Activate Environment**

.. code-block:: bash

   # Activate your environment
   mamba activate sales-empire
   
   # Verify Python version
   python --version  # Should be 3.8+

2. **Navigate to Repository**

.. code-block:: bash

   cd ~/Documents/pythons

3. **Verify API Keys** (Optional)

Your environment already has 100+ API keys configured! Check:

.. code-block:: bash

   # View loaded environment
   env | grep API_KEY | head -5

First Script
------------

Let's run a simple script to verify everything works:

**Instagram Analytics**

.. code-block:: bash

   python instagram-analyze-stats.py

**Leonardo AI Image Generation**

.. code-block:: bash

   python leonardo-api.py --help

**OpenAI Content Analysis**

.. code-block:: bash

   python openai-content-analyzer.py

Common Workflows
----------------

Morning Instagram Routine
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Check growth metrics
   python instagram-analyze-stats.py
   
   # Strategic following
   python instagram-follow-user-followers.py --target competitor
   
   # Engage with community
   python instagram-like-hashtags.py --hashtags art,design

AI Art Production
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Generate batch artwork
   python leonardo-api.py --batch 10
   
   # Upscale images
   python leonardo-upscale-loop.py
   
   # Add watermarks
   python image-add-text-overlay.py --watermark

Music Generation
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Generate music
   python suno-generator.py --prompts ideas.txt
   
   # Organize library
   python suno-music-catalog.py
   
   # Normalize audio levels
   python audio-normalize.py

Troubleshooting
---------------

**Module Not Found**

.. code-block:: bash

   # Install missing dependencies
   pip install -r requirements-py.txt

**API Key Missing**

All keys are in ``~/.env.d/MASTER_CONSOLIDATED.env``. Check:

.. code-block:: bash

   cat ~/.env.d/MASTER_CONSOLIDATED.env | grep YOUR_SERVICE

**Permission Errors**

.. code-block:: bash

   # Make script executable
   chmod +x script-name.py

Next Steps
----------

- Explore :doc:`categories/index` to find scripts by category
- Read :doc:`best-practices` for optimization tips
- Check :doc:`api-services` for available integrations

.. note::
   ?? **Pro Tip**: Use the search function to quickly find scripts by functionality!
