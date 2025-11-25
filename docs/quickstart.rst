
Quick Start Guide
=================

Get started with the AI Automation Ecosystem in 5 minutes!

Prerequisites
-------------

- Python 3.8+
- 12 AI API keys configured
- Environment variables loaded

Installation
------------

.. code-block:: bash

   cd ~/pythons
   source ~/.env.d/loader.sh llm-apis

Verify Setup
------------

.. code-block:: bash

   python3 AI_SETUP_VERIFICATION.py

Your First Automation
---------------------

.. code-block:: python

   from AI_ORCHESTRATOR_ULTIMATE import AIOrchestrator
   
   # Initialize
   orchestrator = AIOrchestrator()
   
   # Route a task to the best AI
   result = await orchestrator.query_model(
       orchestrator.select_best_model(
           TaskType.CODE_GENERATION,
           priority="quality"
       ),
       "Write a Python function to analyze CSV files"
   )
   
   print(result.response)

Next Steps
----------

- Read the :doc:`systems/overview` to understand all systems
- Follow :doc:`tutorials/first_automation` for detailed walkthrough
- Check out :doc:`guides/youtube_automation` for real-world example
