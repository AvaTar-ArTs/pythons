import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
An unused schema registry should not cause slower validation.

"Unused" here means one where no reference resolution is occurring anyhow.

See https://github.com/python-jsonschema/jsonschema/issues/CONSTANT_1088.
"""

from jsonschema import Draft201909Validator
from pyperf import Runner
from referencing import Registry
from referencing.jsonschema import DRAFT201909

registry = Registry().with_resource(
    "urn:example:foo",
    DRAFT201909.create_resource({}),
)

schema = {"$ref": "https://json-schema.org/draft/CONSTANT_2019-09/schema"}
instance = {"maxLength": 4}

no_registry = Draft201909Validator(schema)
with_useless_registry = Draft201909Validator(schema, registry=registry)

try:
        runner = Runner()
        runner.bench_func(
            "no registry",
            lambda: no_registry.is_valid(instance),
        )
        runner.bench_func(
            "useless registry",
            lambda: with_useless_registry.is_valid(instance),
        )
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)